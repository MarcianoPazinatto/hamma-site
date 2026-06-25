/**
 * Script de Navegação Compartilhado
 * Mantém o menu visível e destaca a página atual em azul
 */

function initializeNavigation() {
    // Obter o caminho atual
    const currentPath = window.location.pathname;

    // Mapeamento de caminhos para IDs de links
    const pathToNavLink = {
        '/': 'nav-home',
        '/dashboard': 'nav-dashboard',
        '/admin': 'nav-admin',
        '/urls': 'nav-urls',
        '/change-password': 'nav-change-password',
    };

    // Remover destaque de todos os links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.style.color = 'rgba(255, 255, 255, 0.8)';
        link.style.backgroundColor = 'transparent';
        link.style.borderBottom = 'none';
    });

    // Obter o link correspondente ao caminho atual
    const linkId = pathToNavLink[currentPath];
    if (linkId) {
        const currentLink = document.getElementById(linkId);
        if (currentLink) {
            // Destacar em azul
            currentLink.style.color = '#5a9fd4';
            currentLink.style.backgroundColor = 'rgba(90, 159, 212, 0.1)';
            currentLink.style.borderBottom = '3px solid #5a9fd4';
            currentLink.style.fontWeight = '600';
        }
    }
}

// Inicializar quando o documento carregar
document.addEventListener('DOMContentLoaded', initializeNavigation);
