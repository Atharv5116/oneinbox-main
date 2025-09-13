import { webserver_port } from '../../../sites/common_site_config.json'

export default {
  '^/(app/api/assets/filter/private)': {
    target: `http:127.0.0.1:${webserver_port}`,
    ws: true,
    router: function(req) {
      const site_name = req.headers.host.split(':')[0];
      return `http://${site_name}:${webserver_port}`
    }
  }
}
