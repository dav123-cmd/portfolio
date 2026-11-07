tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: { display: ['PT Sans','sans-serif'], body: ['DM Sans','sans-serif'] },
      colors: { accent: '#FF6B2B', 'accent-light': '#FF8F5C' }
    }
  }
}





function app() {
  return {
    dark: false,
    mm: false,
    sc: false,
    s: 'hero',

    init() {
      // dark mode
      this.dark = localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      this.$watch('dark', v => localStorage.setItem('theme', v ? 'dark' : 'light'));

      // scroll
      window.addEventListener('scroll', () => {
        this.sc = window.scrollY > 20;
        this.updateSection();
      }, { passive: true });

      // reveal
      const io = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
      document.querySelectorAll('.reveal').forEach(el => io.observe(el));

      // year
      document.getElementById('yr').textContent = new Date().getFullYear();
    },

    updateSection() {
      const atBottom = (window.innerHeight + window.scrollY) >= document.body.scrollHeight - 60;
      if (atBottom) { this.s = 'contact'; return; }
      const ids = ['contact','blog','reviews','about','work','services','hero'];
      for (const id of ids) {
        const el = document.getElementById(id);
        if (el && window.scrollY >= el.offsetTop - 130) { this.s = id; return; }
      }
    }
  }
}


const revealElements = document.querySelectorAll('.reveal');

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
  revealElements.forEach(element => revealObserver.observe(element));
} else {
  revealElements.forEach(element => element.classList.add('visible'));
}


 function projects() {
      return {
        dark: false,
        scrolled: false,
        mobileMenu: false,
        filter: 'all',

        filterOptions: [
          { value: 'all',       label: 'All (9)' },
          { value: 'saas',      label: 'SaaS' },
          { value: 'landing',   label: 'Landing page' },
          { value: 'agency',    label: 'Agency' },
          { value: 'ecommerce', label: 'E-commerce' },
        ],

        allProjects: [
          { id:1,  title:'Novu — SaaS Dashboard',  category:'saas',      categoryLabel:'SaaS',         tags:['SaaS','Figma','Tailwind'],           year:'2025', desc:'Complete redesign of a B2B notification platform. Reduced cognitive load by 40% and improved trial-to-paid conversion.',    img:'https://images.unsplash.com/photo-1551650975-87deedd944c3?w=700&q=80',  url:'case-study.html' },
          { id:2,  title:'Finlo — Fintech App',    category:'landing',   categoryLabel:'Landing page', tags:['Landing page','Fintech','Alpine.js'], year:'2024', desc:'Marketing site and onboarding flow for a personal finance app targeting young professionals.',                              img:'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=700&q=80', url:'case-study.html' },
          { id:3,  title:'Orea — Creative Agency', category:'agency',    categoryLabel:'Agency',       tags:['Agency','Animation'],                year:'2024', desc:'Bold editorial site for a Paris-based branding studio. Scroll-driven animations and custom cursor.',                      img:'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=700&q=80', url:'case-study.html' },
          { id:4,  title:'Vesta — Real Estate',    category:'landing',   categoryLabel:'Landing page', tags:['Landing page','Real Estate'],         year:'2024', desc:'Conversion-focused landing page for a proptech startup entering the French market.',                                      img:'https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=700&q=80',  url:'case-study.html' },
          { id:5,  title:'Arkio — SaaS Analytics', category:'saas',      categoryLabel:'SaaS',         tags:['SaaS','Dashboard','Figma'],           year:'2024', desc:'Data visualisation dashboard for a B2B analytics platform. Designed for clarity at high data density.',                img:'https://images.unsplash.com/photo-1581472723648-909f4851d4ae?w=700&q=80', url:'case-study.html' },
          { id:6,  title:'Bloom — E-commerce',     category:'ecommerce', categoryLabel:'E-commerce',   tags:['E-commerce','Shopify'],               year:'2023', desc:'Custom Shopify theme for a sustainable cosmetics brand. Mobile-first with high emphasis on product imagery.',           img:'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=700&q=80',  url:'case-study.html' },
          { id:7,  title:'Mira — Health App',      category:'landing',   categoryLabel:'Landing page', tags:['Landing page','Health','Tailwind'],   year:'2023', desc:'App landing page for a mental wellness startup. Warm, accessible design with strong social proof.',                    img:'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=700&q=80', url:'case-study.html' },
          { id:8,  title:'Noto — Agency Rebrand',  category:'agency',    categoryLabel:'Agency',       tags:['Agency','Rebrand'],                  year:'2023', desc:'Full rebrand and website for a digital communications agency in Lyon.',                                                img:'https://images.unsplash.com/photo-1497366216548-37526070297c?w=700&q=80', url:'case-study.html' },
          { id:9,  title:'Kova — E-commerce',      category:'ecommerce', categoryLabel:'E-commerce',   tags:['E-commerce','Figma'],                year:'2023', desc:'Product page redesign and checkout optimisation for a DTC furniture brand. Reduced cart abandonment by 18%.',         img:'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=700&q=80',  url:'case-study.html' },
        ],

        get visibleCount() {
          if (this.filter === 'all') return this.allProjects.length;
          return this.allProjects.filter(p => p.category === this.filter).length;
        },

        init() {
          this.dark = localStorage.getItem('theme') === 'dark'
            || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);

          window.addEventListener('scroll', () => {
            this.scrolled = window.scrollY > 20;
          }, { passive: true });

          this.$nextTick(() => {
            const obs = new IntersectionObserver(entries => {
              entries.forEach(e => {
                if (e.isIntersecting) {
                  e.target.classList.add('visible');
                  obs.unobserve(e.target);
                }
              });
            }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
            document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
          });
        }
      }
    }
