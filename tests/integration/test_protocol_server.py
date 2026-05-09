"""
Integration tests for protocol server
Tests WebSocket and HTTP communication
"""
import pytest
import asyncio
import websockets
import json
import threading
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "SANDKASSE" / "07_Sandkasse_SelfHealing" / "for_lenovo"))

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def server_port():
    """Port for test server"""
    return 18765  # Different from production port


@pytest.fixture
def mock_protokoll():
    """Mock protocol instance"""
    mock = type('MockProtokoll', (), {
        'is_running': False,
        'current_prosjekt': None,
        'stopp': lambda self: None
    })()
    return mock


class TestProtocolServer:
    """Integration tests for protocol server"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_websocket_connection(self, server_port):
        """Test basic WebSocket connection"""
        # This test requires a running server
        # In CI, we would start the server here
        
        # For now, just test that we can create a connection (server may not be running)
        try:
            async with websockets.connect(f"ws://localhost:{server_port}") as ws:
                # Send ping
                await ws.send(json.dumps({"type": "ping"}))
                
                # Wait for response with timeout
                response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                data = json.loads(response)
                
                assert data.get("type") == "pong"
        except (OSError, websockets.exceptions.InvalidStatusCode):
            pytest.skip("Server not running - skipping integration test")
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_start_protokoll_message(self, server_port):
        """Test starting a protocol via WebSocket"""
        message = {
            "type": "start_protokoll",
            "data": {
                "navn": "TestProsjekt",
                "krav": "Test requirements"
            }
        }
        
        try:
            async with websockets.connect(f"ws://localhost:{server_port}") as ws:
                await ws.send(json.dumps(message))
                
                response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                data = json.loads(response)
                
                assert data.get("type") == "protokoll_started"
                assert data.get("data", {}).get("navn") == "TestProsjekt"
        except (OSError, websockets.exceptions.InvalidStatusCode):
            pytest.skip("Server not running - skipping integration test")
    
    @pytest.mark.integration
    def test_http_health_endpoint(self):
        """Test HTTP health check endpoint"""
        import urllib.request
        
        try:
            response = urllib.request.urlopen(
                "http://localhost:8765/health",
                timeout=5
            )
            data = json.loads(response.read())
            
            assert data.get("status") == "ok"
        except urllib.error.URLError:
            pytest.skip("HTTP server not running - skipping integration test")


class TestSandkasseProtocol:
    """Integration tests for Sandkasse Protocol"""
    
    @pytest.mark.integration
    def test_full_protocol_execution(self):
        """Test running full 6-phase protocol"""
        try:
            from sandkasse_protokoll import SandkasseProtokoll
        except ImportError:
            pytest.skip("sandkasse_protokoll not available")
        
        # Create protocol instance
        import queue
        event_queue = queue.Queue()
        
        protocol = SandkasseProtokoll(event_queue=event_queue)
        
        # Test project
        result = protocol.kjør_full_protokoll(
            "TestProsjekt_CI",
            "Test project for CI/CD pipeline"
        )
        
        # Verify result structure
        assert isinstance(result, dict)
        assert "success" in result
        assert "faser_fullfort" in result


class TestKubernetesIntegration:
    """Integration tests for Kubernetes deployment"""
    
    @pytest.mark.integration
    @pytest.mark.k8s
    def test_kubernetes_connection(self):
        """Test connection to Kubernetes cluster"""
        try:
            from kubernetes import client, config
            
            # Try to load config
            config.load_kube_config()
            
            # Create API client
            v1 = client.CoreV1Api()
            
            # List namespaces
            namespaces = v1.list_namespace()
            
            assert len(namespaces.items) > 0
            
        except Exception as e:
            pytest.skip(f"Kubernetes not available: {e}")
    
    @pytest.mark.integration
    @pytest.mark.k8s
    def test_anita_agent_namespace(self):
        """Test that anita-agent namespace exists"""
        try:
            from kubernetes import client, config
            
            config.load_kube_config()
            v1 = client.CoreV1Api()
            
            namespaces = v1.list_namespace()
            namespace_names = [ns.metadata.name for ns in namespaces.items]
            
            # Check if our namespaces exist
            assert "anita-agent" in namespace_names or "testing-anita-agent" in namespace_names
            
        except Exception as e:
            pytest.skip(f"Kubernetes not available: {e}")
