#!/usr/bin/env python3
"""
Professional website generator matching the SaySo360 template.

Converts Claude AI website specifications into modern, conversion-focused websites
with video heroes, testimonials, service cards, and mobile optimization.
"""

import json
from typing import Optional, List, Dict
import random


def generate_logo_emoji(industry: str) -> str:
    """Generate appropriate emoji icon for the industry."""
    industry_lower = industry.lower()

    logo_map = {
        'hvac': '❄️',
        'heating': '🔥',
        'cooling': '❄️',
        'plumbing': '🔧',
        'electrical': '⚡',
        'roofing': '🏠',
        'cleaning': '🧹',
        'landscaping': '🌿',
        'auto': '🚗',
        'pest': '🐛',
        'restoration': '🏘️',
        'construction': '🏗️',
        'appliance': '🔌',
        'pool': '🏊',
        'carpet': '🧵',
        'painting': '🎨',
        'dental': '😁',
        'medical': '🏥',
        'lawyer': '⚖️',
        'real estate': '🏡',
    }

    for key, emoji in logo_map.items():
        if key in industry_lower:
            return emoji

    return '🏢'  # Default business emoji


def generate_hero_section(lead: dict, spec: dict, primary_color: str, accent_color: str) -> str:
    """Generate the hero section with video background."""

    company_name = lead.get('name', 'Business')
    industry = lead.get('industry', 'Services')
    email = lead.get('email', 'contact@example.com')

    purpose = spec.get('purpose', f'Professional {industry} Services')

    # Extract from spec or create defaults
    seo = spec.get('seo_strategy', {})
    if isinstance(seo, dict):
        keywords = seo.get('keywords', f'{company_name}, {industry}')
    else:
        keywords = f'{company_name}, {industry}'

    phone = lead.get('phone', '(555) 123-4567')

    return f'''<section class="relative min-h-screen overflow-hidden flex items-center justify-center">
    <div class="absolute inset-0 w-full h-full bg-gradient-to-b from-gray-900 via-gray-800 to-gray-900"></div>
    <div class="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/60"></div>

    <div class="relative z-10 text-center text-white px-4 pt-20 pb-10 max-w-4xl mx-auto">
        <div class="inline-flex items-center gap-2 bg-white/10 border border-white/25 backdrop-blur-sm text-white rounded-full px-5 py-2 text-sm font-semibold mb-8">
            <span class="animate-pulse">⚡</span> Limited Same-Day Slots Available
        </div>

        <h1 class="font-bold text-4xl md:text-6xl lg:text-7xl leading-tight mb-6">
            <span style="color: rgb(255, 255, 255); text-shadow: rgba(0, 0, 0, 0.5) 0px 2px 20px;">Your Area's Most Trusted</span><br>
            <span style="color: {accent_color}; text-shadow: {accent_color}80 0px 0px 40px, {accent_color}60 0px 0px 80px, rgba(0, 0, 0, 0.5) 0px 2px 4px;">{industry} Experts</span>
        </h1>

        <p class="text-lg md:text-xl text-white/90 max-w-2xl mx-auto mb-8 leading-relaxed">{purpose}</p>

        <div class="flex flex-wrap justify-center gap-3 mb-8">
            <span class="backdrop-blur-sm bg-white/10 border border-white/20 rounded-full px-4 py-2 text-sm font-medium">✅ Licensed & Insured</span>
            <span class="backdrop-blur-sm bg-white/10 border border-white/20 rounded-full px-4 py-2 text-sm font-medium">⭐ 5★ Google Rating</span>
            <span class="backdrop-blur-sm bg-white/10 border border-white/20 rounded-full px-4 py-2 text-sm font-medium">🚨 Emergency Service</span>
            <span class="backdrop-blur-sm bg-white/10 border border-white/20 rounded-full px-4 py-2 text-sm font-medium">🏆 Award Winner</span>
        </div>

        <div class="flex gap-4 justify-center flex-wrap mb-8">
            <a href="sms:{phone}" class="inline-flex items-center gap-2 bg-{accent_color.replace('#', '')} hover:brightness-110 text-white font-bold text-base md:text-lg px-8 py-4 rounded-xl transition" style="background-color: {accent_color}; box-shadow: {accent_color}80 0px 0px 25px, {accent_color}60 0px 0px 50px, rgba(0, 0, 0, 0.3) 0px 4px 15px;">💬 Text Us Now — {phone}</a>
            <a href="#contact" class="inline-flex items-center gap-2 border-2 border-white text-white font-bold text-base md:text-lg px-8 py-4 rounded-xl hover:bg-white hover:text-gray-900 transition">Get Free Quote →</a>
        </div>

        <p class="text-white/60 text-sm">Trusted by 50+ homeowners in your area</p>
    </div>
</section>'''


def generate_reviews_carousel(reviews_list: List[Dict]) -> str:
    """Generate auto-scrolling reviews carousel."""

    reviews_html = ""
    # Duplicate reviews for infinite scroll effect
    for _ in range(2):
        for review in reviews_list:
            reviews_html += f'''<div class="inline-block min-w-[320px] mx-3 bg-white rounded-xl shadow-md border border-gray-100 p-5 whitespace-normal">
            <div class="flex items-center justify-between mb-2">
                <div class="flex gap-0.5">
                    <span class="text-amber-400 text-sm">★</span>
                    <span class="text-amber-400 text-sm">★</span>
                    <span class="text-amber-400 text-sm">★</span>
                    <span class="text-amber-400 text-sm">★</span>
                    <span class="text-amber-400 text-sm">★</span>
                </div>
                <span class="text-lg font-bold" style="color: rgb(66, 133, 244);">G</span>
            </div>
            <p class="text-gray-700 text-sm leading-relaxed mb-3 line-clamp-3">{review['text']}</p>
            <p class="text-sm font-semibold text-gray-900">{review['author']} <span class="text-blue-500 text-xs ml-1">✓</span></p>
        </div>'''

    return f'''<div class="py-10 bg-white overflow-hidden">
    <style>
        @keyframes scroll {{
            0% {{ transform: translateX(0); }}
            100% {{ transform: translateX(-50%); }}
        }}
        .animate-scroll {{
            animation: scroll 30s linear infinite;
        }}
    </style>
    <div class="animate-scroll flex whitespace-nowrap">
        {reviews_html}
    </div>
</div>'''


def generate_services_section(services_list: List[str], primary_color: str, accent_color: str) -> str:
    """Generate services grid section."""

    service_icons = {
        'repair': '🔧',
        'maintenance': '🛠️',
        'installation': '🏗️',
        'emergency': '🚨',
        'inspection': '🔍',
        'upgrade': '⬆️',
        'replacement': '🔄',
        'cleaning': '🧹',
        'tune': '🎯',
        'restoration': '🔨',
    }

    services_html = ""
    for service in services_list[:6]:
        icon = '🔧'
        for key, emoji in service_icons.items():
            if key in service.lower():
                icon = emoji
                break

        services_html += f'''<div class="group relative rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-all hover:-translate-y-1 duration-300 cursor-pointer">
            <div class="w-full h-48 bg-gradient-to-br from-gray-200 to-gray-300 flex items-center justify-center text-6xl">
                {icon}
            </div>
            <div class="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 to-transparent text-white">
                <h3 class="font-bold text-lg">{service}</h3>
                <p class="text-sm text-white/80 line-clamp-2">Professional {service.lower()} services tailored to your needs.</p>
            </div>
        </div>'''

    return f'''<section id="services" class="py-20 bg-gray-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="text-center mb-12">
            <span class="inline-block bg-{primary_color.replace('#', '')}/10 text-{primary_color.replace('#', '')} rounded-full px-4 py-1 text-sm font-semibold mb-4" style="background-color: {primary_color}20; color: {primary_color};">Our Services</span>
            <h2 class="font-bold text-3xl md:text-4xl text-gray-900 mb-3">Professional Services</h2>
            <p class="text-gray-600 max-w-xl mx-auto">Expert solutions for every need — residential and commercial.</p>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {services_html}
        </div>
        <div class="mt-10 bg-{accent_color.replace('#', '')} rounded-2xl p-8 text-center text-white" style="background-color: {primary_color};">
            <h3 class="font-bold text-2xl mb-3">Need Help Today?</h3>
            <p class="text-white/80 mb-6 max-w-lg mx-auto">Our team is standing by — same-day service available.</p>
            <div class="flex gap-4 justify-center flex-wrap">
                <a href="sms:" class="bg-{accent_color.replace('#', '')} hover:brightness-110 text-white font-bold px-6 py-3 rounded-xl transition" style="background-color: {accent_color};">💬 Text Us Now</a>
                <a href="#contact" class="border-2 border-white text-white font-bold px-6 py-3 rounded-xl hover:bg-white hover:text-gray-900 transition">Call Now</a>
            </div>
        </div>
    </div>
</section>'''


def generate_full_html(lead: dict, spec: dict, reviews: List[Dict] = None) -> str:
    """Generate complete professional website HTML."""

    company_name = lead.get('name', 'Business')
    industry = lead.get('industry', 'Services')
    email = lead.get('email', 'contact@example.com')
    phone = lead.get('phone', '(555) 123-4567')

    # Extract colors from spec or use defaults
    visual = spec.get('visual_design', {})
    if isinstance(visual, dict):
        primary_color = visual.get('primary_color', '#0066cc')
        secondary_color = visual.get('secondary_color', '#ff6b6b')
    else:
        primary_color = '#0066cc'
        secondary_color = '#ff6b6b'

    # Use secondary as accent
    accent_color = secondary_color

    logo_emoji = generate_logo_emoji(industry)

    # Extract services
    content_arch = spec.get('content_architecture', {})
    if isinstance(content_arch, dict):
        services = content_arch.get('pages', []) if isinstance(content_arch.get('pages'), list) else []
    else:
        services = []

    if not services:
        services = ['Emergency Service', 'Repair & Maintenance', 'Installation', 'System Upgrade', 'Preventive Care']

    # Generate sample reviews if not provided
    if not reviews:
        reviews = [
            {'text': f'{company_name} saved us when our system went down. Fixed same day. Absolute lifesavers!', 'author': 'Jennifer K.'},
            {'text': f'Professional, honest, and thorough. Found issues before they became problems. Highly recommend!', 'author': 'Robert D.'},
            {'text': f'Best service in the area. Fair pricing, excellent work, and great customer service. Will use again.', 'author': 'Linda H.'},
            {'text': f'Called on a weekend and they showed up fast. Diagnosed and fixed on the spot. Great team!', 'author': 'Marcus T.'},
            {'text': f'Clear estimates, on-time arrivals, and honest advice. No upsells, just quality work.', 'author': 'Angela P.'},
        ]

    purpose = spec.get('purpose', f'Professional {industry} Services')

    # Create the full HTML
    html = f'''<!DOCTYPE html>
<html lang="en" style="--primary: {primary_color}; --accent: {accent_color};">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{company_name} — Professional {industry} services. Licensed, insured, and ready when you need us most.">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{company_name} — {industry} Services">
    <meta property="og:description" content="Professional {industry} services. 24/7 emergency service available.">
    <meta name="twitter:card" content="summary_large_image">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

    <title>{company_name} — {industry} Services</title>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            line-height: 1.6;
            color: #333;
        }}

        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 50;
            transition: all 0.3s;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        nav .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 72px;
        }}

        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        nav a {{
            color: #666;
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: color 0.3s;
        }}

        nav a:hover {{
            color: var(--primary);
        }}

        .nav-links {{
            display: none;
            gap: 2rem;
        }}

        @media (min-width: 768px) {{
            .nav-links {{
                display: flex;
            }}
        }}

        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.625rem 1.25rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.875rem;
            text-decoration: none;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
        }}

        .cta-primary {{
            background-color: var(--primary);
            color: white;
        }}

        .cta-primary:hover {{
            filter: brightness(1.1);
        }}

        .cta-secondary {{
            border: 2px solid white;
            color: white;
        }}

        .cta-secondary:hover {{
            background-color: white;
            color: var(--primary);
        }}

        body {{
            padding-top: 72px;
        }}

        @media (max-width: 768px) {{
            .mobile-nav {{
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                display: flex;
                height: 56px;
                z-index: 40;
                box-shadow: 0 -4px 20px rgba(0,0,0,0.15);
            }}

            .mobile-nav a {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-weight: 700;
                text-decoration: none;
                color: white;
                font-size: 0.75rem;
            }}

            .mobile-nav a:first-child {{
                background-color: var(--accent);
                border-right: 1px solid rgba(255,255,255,0.15);
            }}

            .mobile-nav a:last-child {{
                background-color: var(--primary);
            }}

            body {{
                padding-bottom: 56px;
            }}
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container">
            <div class="logo">{logo_emoji} {company_name}</div>
            <div class="nav-links">
                <a href="#services">Services</a>
                <a href="#about">About</a>
                <a href="#reviews">Reviews</a>
                <a href="#contact">Contact</a>
            </div>
            <a href="tel:{phone}" class="cta-button cta-primary" style="display: none; margin-left: auto;" id="desktop-call">📞 {phone}</a>
        </div>
    </nav>

    {generate_hero_section(lead, spec, primary_color, accent_color)}

    {generate_reviews_carousel(reviews)}

    {generate_services_section(services, primary_color, accent_color)}

    <section id="about" class="py-20" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white;">
        <div class="max-w-7xl mx-auto px-4">
            <div class="grid md:grid-cols-2 gap-12 items-center">
                <div>
                    <span class="inline-block bg-{accent_color.replace('#', '')}/20 text-{accent_color.replace('#', '')} rounded-full px-4 py-1 text-sm font-semibold mb-4" style="background-color: {accent_color}20; color: {accent_color};">About Us</span>
                    <h2 class="font-bold text-3xl md:text-4xl mb-6 leading-tight">Professional {industry} Services<br><span style="color: {accent_color};">You Can Trust</span></h2>
                    <p class="text-white/80 leading-relaxed mb-4">{company_name} has been serving the community with professional, reliable service. We treat every customer like family.</p>
                    <p class="text-white/80 leading-relaxed mb-6">Our team of licensed professionals is committed to transparent pricing, quality workmanship, and 100% customer satisfaction.</p>
                    <a href="#contact" class="inline-flex items-center gap-2 cta-button cta-primary">Get a Free Quote →</a>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div class="rounded-2xl p-6 text-center" style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                        <div class="text-3xl md:text-4xl font-bold text-{accent_color.replace('#', '')} mb-1" style="color: {accent_color};">10+</div>
                        <div class="text-white/70 text-sm">Years Experience</div>
                    </div>
                    <div class="rounded-2xl p-6 text-center" style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                        <div class="text-3xl md:text-4xl font-bold text-{accent_color.replace('#', '')} mb-1" style="color: {accent_color};">500+</div>
                        <div class="text-white/70 text-sm">Happy Customers</div>
                    </div>
                    <div class="rounded-2xl p-6 text-center" style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                        <div class="text-3xl md:text-4xl font-bold text-{accent_color.replace('#', '')} mb-1" style="color: {accent_color};">✓</div>
                        <div class="text-white/70 text-sm">Licensed & Insured</div>
                    </div>
                    <div class="rounded-2xl p-6 text-center" style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);">
                        <div class="text-3xl md:text-4xl font-bold text-{accent_color.replace('#', '')} mb-1" style="color: {accent_color};">5★</div>
                        <div class="text-white/70 text-sm">Google Rating</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="py-20" style="background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%); color: white;">
        <div class="max-w-6xl mx-auto px-4 grid md:grid-cols-2 gap-12">
            <div>
                <span class="inline-block bg-{accent_color.replace('#', '')}/20 text-{accent_color.replace('#', '')} rounded-full px-4 py-1 text-sm font-semibold mb-4" style="background-color: {accent_color}20; color: {accent_color};">Contact Us</span>
                <h2 class="font-bold text-3xl md:text-4xl mb-6">Get Your Free<br>Estimate Today</h2>
                <div class="space-y-5">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center text-lg">📞</div>
                        <div>
                            <div class="text-white/50 text-xs uppercase tracking-wider">Phone</div>
                            <a href="tel:{phone}" class="text-white font-semibold hover:text-{accent_color.replace('#', '')} transition" style="color: white;">{phone}</a>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center text-lg">✉️</div>
                        <div>
                            <div class="text-white/50 text-xs uppercase tracking-wider">Email</div>
                            <a href="mailto:{email}" class="text-white font-semibold hover:text-{accent_color.replace('#', '')} transition" style="color: white;">{email}</a>
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-xl bg-white/10 flex items-center justify-center text-lg">🕐</div>
                        <div>
                            <div class="text-white/50 text-xs uppercase tracking-wider">Hours</div>
                            <div class="text-white font-semibold">Mon-Sat: 8AM - 6PM<br>24/7 Emergency Service</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="rounded-2xl p-6 md:p-8" style="background: rgba(0,0,0,0.3); backdrop-filter: blur(10px);">
                <form class="space-y-4" action="mailto:{email}" method="POST" enctype="text/plain">
                    <input type="text" placeholder="Your Name" required class="w-full rounded-xl px-4 py-3 bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-{accent_color.replace('#', '')} focus:outline-none transition" style="border-color: rgba(255,255,255,0.1); background-color: rgba(0,0,0,0.3);">
                    <input type="tel" placeholder="Phone Number" required class="w-full rounded-xl px-4 py-3 bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-{accent_color.replace('#', '')} focus:outline-none transition" style="border-color: rgba(255,255,255,0.1); background-color: rgba(0,0,0,0.3);">
                    <textarea placeholder="How can we help?" rows="3" class="w-full rounded-xl px-4 py-3 bg-gray-700 border border-gray-600 text-white placeholder-gray-400 focus:border-{accent_color.replace('#', '')} focus:outline-none transition resize-none" style="border-color: rgba(255,255,255,0.1); background-color: rgba(0,0,0,0.3);"></textarea>
                    <button type="submit" class="w-full cta-button cta-primary" style="background-color: {accent_color}; justify-content: center;">Send Message →</button>
                </form>
            </div>
        </div>
    </section>

    <footer style="background: linear-gradient(135deg, var(--primary) 0%, #1a1a2e 100%); color: white; padding: 2rem;">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p>&copy; 2024 {company_name}. All rights reserved. | {industry} Services</p>
            <p class="text-white/60 text-sm mt-2">Professional service you can trust</p>
        </div>
    </footer>

    <!-- Mobile Bottom Nav -->
    <div class="mobile-nav" style="display: none;">
        <a href="sms:{phone}">💬 Text Us</a>
        <a href="tel:{phone}">📞 Call Us</a>
    </div>

    <script>
        // Show mobile nav only on mobile
        const mobileNav = document.querySelector('.mobile-nav');
        if (window.innerWidth < 768) {{
            mobileNav.style.display = 'flex';
        }}

        window.addEventListener('resize', () => {{
            if (window.innerWidth < 768) {{
                mobileNav.style.display = 'flex';
            }} else {{
                mobileNav.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>'''

    return html


def save_websites_to_html(results: dict, output_dir: str = "generated_websites"):
    """Save HTML files for each lead's website."""
    import os

    os.makedirs(output_dir, exist_ok=True)

    for item in results.get('website_specs', []):
        lead = item['lead']
        spec = item['website_spec']

        filename = lead.get('name', 'website').replace(' ', '_').lower()
        filepath = os.path.join(output_dir, f"{filename}.html")

        html = generate_full_html(lead, spec)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✨ Generated professional website for {lead.get('name', 'Unknown')}: {filepath}")


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python website_generator.py <results_json_file> [output_directory]")
        sys.exit(1)

    results_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "generated_websites"

    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)

    print(f"📄 Loading results from {results_file}")
    save_websites_to_html(results, output_dir)
    print(f"✅ Generated {len(results.get('website_specs', []))} professional websites in {output_dir}/")

