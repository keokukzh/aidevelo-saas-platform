export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Add security headers
    const response = await fetch(request);
    const newResponse = new Response(response.body, response);
    
    newResponse.headers.set('X-Frame-Options', 'DENY');
    newResponse.headers.set('X-Content-Type-Options', 'nosniff');
    newResponse.headers.set('X-XSS-Protection', '1; mode=block');
    newResponse.headers.set('Strict-Transport-Security', 'max-age=31536000');
    
    // Analytics tracking
    if (url.pathname.includes('/contact') || url.pathname.includes('/demo')) {
      // Log enterprise inquiries
      console.log(`Enterprise inquiry: ${url.pathname} from ${request.headers.get('CF-Connecting-IP')}`);
    }
    
    return newResponse;
  },
};