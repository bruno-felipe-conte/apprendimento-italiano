// ============================================================
// onboarding.js — 3-Slide Educational Onboarding
// ============================================================

const Onboarding = {
  STORAGE_KEY: 'it_onboarding_done',
  slideAtual: 0,

  deveExibir() {
    try {
      return !localStorage.getItem(this.STORAGE_KEY);
    } catch (e) {
      return true;
    }
  },

  mostrar() {
    const modal = document.getElementById('onboarding-modal');
    if (modal) {
      modal.style.display = 'flex';
      this.slideAtual = 0;
      this.atualizarSlides();
    }
  },

  concluir() {
    try {
      localStorage.setItem(this.STORAGE_KEY, '1');
    } catch (e) {}
    const modal = document.getElementById('onboarding-modal');
    if (modal) modal.style.display = 'none';

    // Tour só inicia quando o usuário clicar em ❓ no header
  },

  proximoSlide() {
    const slides = document.querySelectorAll('.onb-slide');
    if (this.slideAtual < slides.length - 1) {
      this.slideAtual++;
      this.atualizarSlides();
    } else {
      this.concluir();
    }
  },

  anteriorSlide() {
    if (this.slideAtual > 0) {
      this.slideAtual--;
      this.atualizarSlides();
    }
  },

  irParaSlide(index) {
    this.slideAtual = index;
    this.atualizarSlides();
  },

  atualizarSlides() {
    const slides = document.querySelectorAll('.onb-slide');
    const dots = document.querySelectorAll('.onb-dot');
    
    slides.forEach((slide, idx) => {
      slide.classList.toggle('active', idx === this.slideAtual);
    });

    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === this.slideAtual);
    });

    // Control button visibility / labels
    const btnPrev = document.getElementById('onb-btn-prev');
    const btnNext = document.getElementById('onb-btn-next');
    
    if (btnPrev) {
      btnPrev.style.visibility = this.slideAtual === 0 ? 'hidden' : 'visible';
    }
    
    if (btnNext) {
      if (this.slideAtual === slides.length - 1) {
        btnNext.textContent = 'Iniziare! 🚀';
      } else {
        btnNext.textContent = 'Avanti →';
      }
    }
  }
};
