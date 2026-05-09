/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8765/:path*',
      },
    ];
  },
  // For statisk export (valgfritt)
  // output: 'export',
  // distDir: 'dist',
};

module.exports = nextConfig;
