/**
 * Cloudflare Worker to serve generated websites from Upstash Redis
 * Provides fast, globally distributed access to generated websites
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // Health check
    if (pathname === '/health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Serve website by ID: /website/{id}
    if (pathname.startsWith('/website/')) {
      const websiteId = pathname.split('/').pop();

      if (!websiteId) {
        return new Response('Not found', { status: 404 });
      }

      try {
        // Try to get from Upstash Redis
        const htmlContent = await getFromRedis(env, `website:${websiteId}`);

        if (htmlContent) {
          return new Response(htmlContent, {
            status: 200,
            headers: {
              'Content-Type': 'text/html; charset=utf-8',
              'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
              'X-Content-Type-Options': 'nosniff',
              'X-Frame-Options': 'SAMEORIGIN',
              'Referrer-Policy': 'no-referrer-when-downgrade'
            }
          });
        }

        return new Response('Website not found', { status: 404 });
      } catch (error) {
        console.error('Error fetching website:', error);
        return new Response('Error fetching website', { status: 500 });
      }
    }

    // Redirect root to dashboard
    if (pathname === '/') {
      return new Response('Redirect to dashboard', {
        status: 302,
        headers: { 'Location': '/dashboard' }
      });
    }

    return new Response('Not found', { status: 404 });
  }
};

/**
 * Get content from Upstash Redis
 */
async function getFromRedis(env, key) {
  const redisUrl = env.UPSTASH_REDIS_URL;

  if (!redisUrl) {
    throw new Error('UPSTASH_REDIS_URL not configured');
  }

  // Parse Redis URL: redis://:password@host:port
  const url = new URL(redisUrl);
  const command = `GET ${key}`;

  const response = await fetch(redisUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      commands: [['GET', key]]
    })
  });

  if (!response.ok) {
    throw new Error(`Redis request failed: ${response.statusText}`);
  }

  const data = await response.json();
  const result = data.result && data.result[0];

  return result || null;
}
