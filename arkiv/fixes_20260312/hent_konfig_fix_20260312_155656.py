@heal
def hent_konfig(nøkkel):
    """
    Henter konfigurasjonsverdi
    Kan feile med KeyError
    """
    config = {
        "database_url": "postgresql://localhost/db",
        "timeout": 30,
        "retry_count": 3
    }
    
    print(f"[CONF] Henter konfig for '{nøkkel}'...")
    return config[nøkkel]  # Kan feile hvis nøkkel ikke finnes
