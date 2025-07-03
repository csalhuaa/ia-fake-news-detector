
        // Create animated particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 50;

            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Form submission handler
        document.getElementById('analysisForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const form = e.target;
            const formData = new FormData(form);
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            
            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analizando...';
            loading.style.display = 'block';
            results.style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show results
                    const resultCard = document.createElement('div');
                    resultCard.className = `result-card ${data.es_verdadera ? 'real-news' : 'fake-news'}`;
                    
                    const icon = data.es_verdadera ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle';
                    const status = data.es_verdadera ? 'NOTICIA PROBABLEMENTE VERDADERA' : 'NOTICIA PROBABLEMENTE FALSA';
                    const statusIcon = data.es_verdadera ? '✅' : '⚠️';
                    
                    let detailHTML = '';
                    if (data.modelo_usado === 'both' && data.resultados_detalle.length > 1) {
                        detailHTML = `
                            <div class="result-detail">
                                <strong>Análisis detallado:</strong>
                                ${data.resultados_detalle.map(resultado => `
                                    <div class="model-result">
                                        <strong>${resultado.modelo}:</strong> ${resultado.prediccion} (${resultado.confianza}%)
                                    </div>
                                `).join('')}
                            </div>
                        `;
                    }
                    
                    resultCard.innerHTML = `
                        <div class="result-title">
                            <i class="${icon}"></i>
                            Resultado del Análisis
                        </div>
                        <div class="result-content">
                            <strong>${statusIcon} ${status}</strong><br>
                            <strong>Confianza:</strong> ${data.confianza}%<br>
                            <strong>Modelo usado:</strong> ${data.modelo_usado.toUpperCase()}<br>
                            <strong>Texto analizado:</strong> "${data.texto_analizado}"
                            ${detailHTML}
                        </div>
                    `;
                    
                    results.innerHTML = '';
                    results.appendChild(resultCard);
                    results.style.display = 'block';
                    
                } else {
                    // Show error
                    const errorCard = document.createElement('div');
                    errorCard.className = 'error-card';
                    errorCard.innerHTML = `
                        <div class="result-title">
                            <i class="fas fa-exclamation-circle"></i>
                            Error en el Análisis
                        </div>
                        <div class="result-content">
                            <strong>❌ Error:</strong> ${data.error}
                        </div>
                    `;
                    
                    results.innerHTML = '';
                    results.appendChild(errorCard);
                    results.style.display = 'block';
                }
                
            } catch (error) {
                console.error('Error:', error);
                
                const errorCard = document.createElement('div');
                errorCard.className = 'error-card';
                errorCard.innerHTML = `
                    <div class="result-title">
                        <i class="fas fa-exclamation-circle"></i>
                        Error de Conexión
                    </div>
                    <div class="result-content">
                        <strong>❌ Error:</strong> No se pudo conectar con el servidor. Por favor, inténtalo de nuevo.
                    </div>
                `;
                
                results.innerHTML = '';
                results.appendChild(errorCard);
                results.style.display = 'block';
            } finally {
                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analizar Noticia';
                loading.style.display = 'none';
            }
        });

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initialize particles when page loads
        window.addEventListener('load', function() {
            createParticles();
        });

        // Add floating animation to feature items
        const featureItems = document.querySelectorAll('.feature-item');
        featureItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.2}s`;
        });

        // Add typing effect to hero title (optional enhancement)
        function typeWriter(element, text, speed = 100) {
            let i = 0;
            element.innerHTML = '';
            
            function type() {
                if (i < text.length) {
                    element.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                }
            }
            
            type();
        }

        // Optional: Add typing effect to hero title
        // Uncomment the following lines if you want a typing effect:
        /*
        window.addEventListener('load', function() {
            const heroTitle = document.querySelector('.hero-title');
            const originalText = heroTitle.textContent;
            typeWriter(heroTitle, originalText, 100);
        });
        */