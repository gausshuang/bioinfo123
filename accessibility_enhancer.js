// 可访问性增强脚本
// 提升生物信息导航页面的无障碍访问体验

class AccessibilityEnhancer {
    constructor() {
        this.init();
    }
    
    init() {
        this.enhanceKeyboardNavigation();
        this.improveScreenReaderSupport();
        this.addAriaLabels();
        this.enhanceFocusManagement();
        this.addSkipLinks();
        this.improveColorContrast();
        this.addVoiceAnnouncements();
        
        console.log('♿ 可访问性增强功能已启用');
    }
    
    // 增强键盘导航
    enhanceKeyboardNavigation() {
        // 为所有可交互元素添加键盘支持
        document.addEventListener('keydown', (e) => {
            // ESC键关闭模态框和工具提示
            if (e.key === 'Escape') {
                this.closeModals();
                this.hideTooltips();
            }
            
            // Enter键激活按钮
            if (e.key === 'Enter') {
                const focused = document.activeElement;
                if (focused.classList.contains('category-filter')) {
                    focused.click();
                }
            }
            
            // 箭头键导航
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                this.handleArrowNavigation(e);
            }
        });
        
        // 添加可见的焦点指示器
        const focusCSS = `
            <style>
                /* 增强焦点可见性 */
                *:focus {
                    outline: 2px solid #2c5aa0 !important;
                    outline-offset: 2px !important;
                }
                
                .database-card:focus-within {
                    box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.3) !important;
                }
                
                .btn:focus {
                    box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.3) !important;
                }
                
                .search-input:focus {
                    box-shadow: 0 0 0 3px rgba(44, 90, 160, 0.3) !important;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', focusCSS);
    }
    
    // 处理箭头键导航
    handleArrowNavigation(e) {
        const cards = Array.from(document.querySelectorAll('.database-card'));
        const currentIndex = cards.findIndex(card => card.contains(document.activeElement));
        
        if (currentIndex === -1) return;
        
        let nextIndex;
        const cardsPerRow = Math.floor(window.innerWidth / 370); // 估算每行卡片数
        
        switch (e.key) {
            case 'ArrowUp':
                nextIndex = currentIndex - cardsPerRow;
                break;
            case 'ArrowDown':
                nextIndex = currentIndex + cardsPerRow;
                break;
            case 'ArrowLeft':
                nextIndex = currentIndex - 1;
                break;
            case 'ArrowRight':
                nextIndex = currentIndex + 1;
                break;
        }
        
        if (nextIndex >= 0 && nextIndex < cards.length) {
            e.preventDefault();
            const nextCard = cards[nextIndex];
            const focusableElement = nextCard.querySelector('a, button');
            if (focusableElement) {
                focusableElement.focus();
            }
        }
    }
    
    // 改善屏幕阅读器支持
    improveScreenReaderSupport() {
        // 添加页面地标
        const landmarks = {
            'header': 'banner',
            'main': 'main',
            'aside': 'complementary',
            'footer': 'contentinfo'
        };
        
        Object.entries(landmarks).forEach(([selector, role]) => {
            const element = document.querySelector(selector);
            if (element && !element.getAttribute('role')) {
                element.setAttribute('role', role);
            }
        });
        
        // 为搜索区域添加标签
        const searchSection = document.querySelector('.search-section');
        if (searchSection) {
            searchSection.setAttribute('role', 'search');
            searchSection.setAttribute('aria-label', '生物信息资源搜索');
        }
        
        // 为数据库网格添加标签
        const databasesGrid = document.getElementById('databasesGrid');
        if (databasesGrid) {
            databasesGrid.setAttribute('role', 'grid');
            databasesGrid.setAttribute('aria-label', '生物信息资源列表');
            databasesGrid.setAttribute('aria-live', 'polite');
        }
    }
    
    // 添加ARIA标签
    addAriaLabels() {
        // 搜索输入框
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.setAttribute('aria-label', '搜索生物信息资源');
            searchInput.setAttribute('aria-describedby', 'search-help');
            
            // 添加搜索帮助文本
            const helpText = document.createElement('div');
            helpText.id = 'search-help';
            helpText.className = 'sr-only';
            helpText.textContent = '输入关键词搜索893个生物信息资源，包括数据库名称和描述';
            searchInput.parentNode.appendChild(helpText);
        }
        
        // 搜索按钮
        const searchBtn = document.getElementById('searchBtn');
        if (searchBtn) {
            searchBtn.setAttribute('aria-label', '执行搜索');
        }
        
        // 分类筛选器
        document.querySelectorAll('.category-filter').forEach((filter, index) => {
            const categoryName = filter.querySelector('span').textContent;
            const count = filter.querySelector('.category-count').textContent;
            filter.setAttribute('aria-label', `筛选${categoryName}，共${count}个资源`);
            filter.setAttribute('role', 'button');
            filter.setAttribute('tabindex', '0');
        });
        
        // 数据库卡片
        this.enhanceDatabaseCards();
    }
    
    // 增强数据库卡片的可访问性
    enhanceDatabaseCards() {
        // 监听卡片渲染
        document.addEventListener('databasesRendered', () => {
            document.querySelectorAll('.database-card').forEach((card, index) => {
                const name = card.querySelector('.database-name').textContent.trim();
                const category = card.querySelector('.database-category').textContent;
                const description = card.querySelector('.database-description').textContent;
                
                card.setAttribute('role', 'article');
                card.setAttribute('aria-label', `${name}，${category}类别，${description}`);
                card.setAttribute('tabindex', '0');
                
                // 为按钮添加更好的标签
                const accessBtn = card.querySelector('.btn-primary');
                if (accessBtn) {
                    accessBtn.setAttribute('aria-label', `访问${name}数据库或网站`);
                }
                
                const favoriteBtn = card.querySelector('.btn-secondary');
                if (favoriteBtn) {
                    favoriteBtn.setAttribute('aria-label', `收藏${name}`);
                }
            });
        });
    }
    
    // 增强焦点管理
    enhanceFocusManagement() {
        // 模态框焦点陷阱
        document.addEventListener('keydown', (e) => {
            const modal = document.querySelector('[style*="position: fixed"][style*="z-index: 10000"]');
            if (modal && e.key === 'Tab') {
                this.trapFocus(modal, e);
            }
        });
        
        // 搜索后焦点管理
        const originalHandleSearch = window.handleSearch;
        if (originalHandleSearch) {
            window.handleSearch = function() {
                originalHandleSearch.call(this);
                // 搜索后将焦点移到结果区域
                setTimeout(() => {
                    const firstCard = document.querySelector('.database-card');
                    if (firstCard) {
                        firstCard.focus();
                        // 宣布搜索结果
                        this.announceSearchResults();
                    }
                }, 100);
            }.bind(this);
        }
    }
    
    // 焦点陷阱
    trapFocus(modal, e) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey) {
            if (document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            }
        } else {
            if (document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    }
    
    // 添加跳转链接
    addSkipLinks() {
        const skipLinks = `
            <div class="skip-links" style="
                position: absolute;
                top: -40px;
                left: 6px;
                background: #2c5aa0;
                color: white;
                padding: 8px;
                z-index: 10000;
                text-decoration: none;
                border-radius: 4px;
                transition: top 0.3s;
            ">
                <a href="#main-content" style="color: white; text-decoration: none;">跳转到主内容</a>
            </div>
            <style>
                .skip-links:focus-within {
                    top: 6px !important;
                }
            </style>
        `;
        
        document.body.insertAdjacentHTML('afterbegin', skipLinks);
        
        // 为主内容添加ID
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.id = 'main-content';
            mainContent.setAttribute('tabindex', '-1');
        }
    }
    
    // 改善颜色对比度
    improveColorContrast() {
        // 添加高对比度模式切换
        const contrastToggle = `
            <button id="contrast-toggle" style="
                position: fixed;
                top: 20px;
                right: 80px;
                background: #2c5aa0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                cursor: pointer;
                font-size: 12px;
                z-index: 1000;
            " aria-label="切换高对比度模式">
                🎨 对比度
            </button>
        `;
        
        document.body.insertAdjacentHTML('beforeend', contrastToggle);
        
        document.getElementById('contrast-toggle').addEventListener('click', () => {
            document.body.classList.toggle('high-contrast');
        });
        
        // 高对比度样式
        const contrastCSS = `
            <style>
                .high-contrast {
                    filter: contrast(150%) !important;
                }
                
                .high-contrast .database-card {
                    border: 2px solid #000 !important;
                }
                
                .high-contrast .btn {
                    border: 2px solid #000 !important;
                }
                
                .high-contrast .category-filter {
                    border: 1px solid #000 !important;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', contrastCSS);
    }
    
    // 添加语音播报
    addVoiceAnnouncements() {
        // 创建屏幕阅读器专用的播报区域
        const announcer = document.createElement('div');
        announcer.id = 'announcer';
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        announcer.className = 'sr-only';
        document.body.appendChild(announcer);
        
        // 添加屏幕阅读器专用样式
        const srOnlyCSS = `
            <style>
                .sr-only {
                    position: absolute !important;
                    width: 1px !important;
                    height: 1px !important;
                    padding: 0 !important;
                    margin: -1px !important;
                    overflow: hidden !important;
                    clip: rect(0, 0, 0, 0) !important;
                    white-space: nowrap !important;
                    border: 0 !important;
                }
            </style>
        `;
        document.head.insertAdjacentHTML('beforeend', srOnlyCSS);
    }
    
    // 宣布搜索结果
    announceSearchResults() {
        const announcer = document.getElementById('announcer');
        const resultCount = document.querySelectorAll('.database-card').length;
        
        if (announcer) {
            announcer.textContent = `搜索完成，找到${resultCount}个匹配的生物信息资源`;
        }
    }
    
    // 关闭模态框
    closeModals() {
        const modals = document.querySelectorAll('[style*="position: fixed"][style*="z-index: 10000"]');
        modals.forEach(modal => modal.remove());
    }
    
    // 隐藏工具提示
    hideTooltips() {
        const tooltips = document.querySelectorAll('.tooltip');
        tooltips.forEach(tooltip => tooltip.classList.remove('show'));
    }
    
    // 检查可访问性
    checkAccessibility() {
        const issues = [];
        
        // 检查图片alt属性
        document.querySelectorAll('img').forEach(img => {
            if (!img.getAttribute('alt')) {
                issues.push('图片缺少alt属性');
            }
        });
        
        // 检查表单标签
        document.querySelectorAll('input').forEach(input => {
            if (!input.getAttribute('aria-label') && !input.getAttribute('aria-labelledby')) {
                const label = document.querySelector(`label[for="${input.id}"]`);
                if (!label) {
                    issues.push('输入框缺少标签');
                }
            }
        });
        
        // 检查颜色对比度（简化版）
        const lightColors = ['#fff', '#ffffff', 'white', 'rgb(255, 255, 255)'];
        document.querySelectorAll('*').forEach(el => {
            const style = getComputedStyle(el);
            const bgColor = style.backgroundColor;
            const textColor = style.color;
            
            if (lightColors.includes(bgColor.toLowerCase()) && lightColors.includes(textColor.toLowerCase())) {
                issues.push('可能存在颜色对比度不足的问题');
            }
        });
        
        if (issues.length > 0) {
            console.warn('⚠️ 发现可访问性问题:', issues);
        } else {
            console.log('✅ 可访问性检查通过');
        }
        
        return issues;
    }
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.accessibilityEnhancer = new AccessibilityEnhancer();
    });
} else {
    window.accessibilityEnhancer = new AccessibilityEnhancer();
}

// 导出类
window.AccessibilityEnhancer = AccessibilityEnhancer;
