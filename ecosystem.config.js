// Configuración de pm2 para la instancia EC2 (Ubuntu).
// interpreter "none": pm2 ejecuta el binario de uvicorn tal cual,
// sin intentar correrlo con Node.
module.exports = {
  apps: [
    {
      name: "api-tienda",
      script: "venv/bin/uvicorn",
      args: "app.main:app --host 0.0.0.0 --port 8010",
      interpreter: "none",
      cwd: "/home/ubuntu/api-tienda",
      autorestart: true,
    },
  ],
};
