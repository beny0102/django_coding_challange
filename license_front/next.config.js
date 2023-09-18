/** @type {import('next').NextConfig} */
const nextConfig = () => {
  return{
      reactStrictMode: true,
      async rewrites(){
          return[
              {
                  source: '/api/:path*',
                  destination: 'http://license-server:8080/api/:path*/'
              }
          ]
      }
  }
}
module.exports = nextConfig
