<template>
  <div>
    <HeroSection />
    <HomePageSale />
    <FeatureSection />
  </div>
</template>

<script>
import FeatureSection from '@/components/Template/FeatureSection.vue';
import HeroSection from '@/components/Template/HeroSection.vue';
import HomePageSale from '@/components/HomePageSale.vue';

export default {
  name: 'HomePage',
  components: {
    HeroSection,
    FeatureSection,
    HomePageSale
  },
  mounted() {
    // Imposta il titolo della pagina
    document.title = "Monitoraggio Prezzi Amazon - Trova Offerte e Sconti in Tempo Reale";

    // Definizione dei meta tag SEO
    const metaTags = [
      { name: "description", content: "Monitora i prezzi su Amazon con il nostro strumento gratuito. Ricevi notifiche sui ribassi, confronta l'andamento dei prezzi e acquista al momento giusto!" },
      { name: "keywords", content: "monitoraggio prezzi Amazon, sconti Amazon, offerte Amazon, tracking prezzi, Amazon price tracker" },
      { name: "robots", content: "index, follow" },
      { property: "og:title", content: "Monitoraggio Prezzi Amazon - Trova Offerte e Sconti in Tempo Reale" },
      { property: "og:description", content: "Monitora i prezzi su Amazon con il nostro strumento gratuito. Ricevi notifiche sui ribassi e acquista al miglior prezzo." },
      { property: "og:url", content: "https://www.pricehub.it/" },
      { property: "og:image", content: "https://www.pricehub.it/assets/amazon-price-tracker.jpg" },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
      { name: "twitter:title", content: "Monitoraggio Prezzi Amazon - Trova Offerte e Sconti in Tempo Reale" },
      { name: "twitter:description", content: "Scopri il miglior momento per acquistare con il nostro tracker prezzi Amazon." },
      { name: "twitter:image", content: "https://www.pricehub.it/assets/amazon-price-tracker.jpg" },
      { name: "viewport", content: "width=device-width, initial-scale=1" } // Mobile-friendly meta tag
    ];

    // Rimuove eventuali meta tag duplicati
    document.querySelectorAll("meta[name], meta[property]").forEach(meta => meta.remove());

    // Aggiunge nuovi meta tag SEO
    metaTags.forEach(tag => {
      const meta = document.createElement("meta");
      if (tag.name) {
        meta.setAttribute("name", tag.name);
      } else if (tag.property) {
        meta.setAttribute("property", tag.property);
      }
      meta.setAttribute("content", tag.content);
      document.head.appendChild(meta);
    });

    // Aggiunge il link canonical
    let canonical = document.querySelector("link[rel='canonical']");
    if (!canonical) {
      canonical = document.createElement("link");
      canonical.setAttribute("rel", "canonical");
      document.head.appendChild(canonical);
    }
    canonical.setAttribute("href", "https://www.pricehub.it/");
  }
};
</script>
