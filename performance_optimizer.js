// 性能优化脚本
// 优化893个生物信息资源的加载和渲染性能

class PerformanceOptimizer {
    constructor() {
        this.isOptimized = false;
        this.lazyLoadOffset = 100; // 预加载偏移量
        this.batchSize = 50; // 批量渲染数量
        this.debounceDelay = 300; // 防抖延迟
        
        this.init();
    }
    
    init() {
        this.optimizeDataLoading();
        this.setupLazyLoading();
        this.optimizeSearch();
        this.setupVirtualScrolling();
        this.preloadCriticalResources();
        this.isOptimized = true;
    }
    
    // 优化数据加载
    optimizeDataLoading() {
        // 重写原始的loadDatabases函数
        const originalLoadDatabases = window.loadDatabases;
        
        window.loadDatabases = async function() {
            try {
                // 显示加载指示器
                const loadingElement = document.getElementById('databasesGrid');
                loadingElement.innerHTML = `
                    <div class="loading-optimized" style="
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        padding: 3rem;
                        color: #666;
                    ">
                        <div class="spinner" style="
                            width: 40px;
                            height: 40px;
                            border: 3px solid #f3f3f3;
                            border-top: 3px solid #2c5aa0;
                            border-radius: 50%;
                            animation: spin 1s linear infinite;
                            margin-bottom: 1rem;
                        "></div>
                        <p>正在加载893个生物信息资源...</p>
                        <p style="font-size: 0.9rem; opacity: 0.7;">优化加载中，请稍候</p>
                    </div>
                `;
                
                // 异步加载数据
                const response = await fetch('databases_processed.json');
                const data = await response.json();
                
                // 数据预处理
                window.allDatabases = this.preprocessData(data);
                window.filteredDatabases = [...window.allDatabases];
                
                // 批量渲染
                this.renderInBatches(window.allDatabases);
                
                // 渲染分类筛选器
                renderCategoryFilters();
                
            } catch (error) {
                console.error('优化加载数据库数据失败:', error);
                // 降级到原始加载方法
                if (originalLoadDatabases) {
                    originalLoadDatabases.call(this);
                }
            }
        }.bind(this);
    }
    
    // 数据预处理
    preprocessData(data) {
        return data.map(item => {
            // 预计算常用值
            item._searchText = (item.name + ' ' + item.short_description + ' ' + (item.short_description_zh || '')).toLowerCase();
            item._resourceIcon = item.resource_type === 'database' ? 'fas fa-database' : 'fas fa-globe-americas';
            item._resourceText = item.resource_type === 'database' ? '访问数据库' : '访问网站';
            
            return item;
        });
    }
    
    // 批量渲染
    renderInBatches(databases) {
        const grid = document.getElementById('databasesGrid');
        grid.innerHTML = '';
        
        let currentBatch = 0;
        const totalBatches = Math.ceil(databases.length / this.batchSize);
        
        const renderNextBatch = () => {
            const start = currentBatch * this.batchSize;
            const end = Math.min(start + this.batchSize, databases.length);
            const batch = databases.slice(start, end);
            
            const fragment = document.createDocumentFragment();
            
            batch.forEach(db => {
                const card = this.createDatabaseCard(db);
                fragment.appendChild(card);
            });
            
            grid.appendChild(fragment);
            
            currentBatch++;
            
            // 更新进度
            if (currentBatch < totalBatches) {
                // 使用requestAnimationFrame确保流畅渲染
                requestAnimationFrame(renderNextBatch);
            } else {
                // 渲染完成
                this.onRenderComplete();
            }
        };
        
        renderNextBatch();
    }
    
    // 创建数据库卡片（优化版本）
    createDatabaseCard(db) {
        const card = document.createElement('div');
        card.className = 'database-card';
        card.setAttribute('data-category', db.category);
        card.setAttribute('data-type', db.resource_type || 'database');
        
        card.innerHTML = `
            <div class="database-header">
                <div>
                    <div class="database-name">
                        <i class="${db._resourceIcon}" style="margin-right: 8px; color: #666; font-size: 0.9rem;"></i>
                        ${db.name}
                    </div>
                    <div class="database-category">${db.category_name}</div>
                </div>
            </div>
            <div class="database-description" data-tooltip="${db.short_description_zh || db.short_description}">
                ${db.short_description}
            </div>
            <div class="database-actions">
                <a href="${db.url}" target="_blank" class="btn btn-primary">
                    <i class="fas fa-external-link-alt"></i>
                    ${db._resourceText}
                </a>
                <button class="btn btn-secondary" onclick="toggleFavorite('${db.id}')">
                    <i class="far fa-heart"></i>
                    收藏
                </button>
            </div>
        `;
        
        return card;
    }
    
    // 渲染完成后的处理
    onRenderComplete() {
        // 更新统计信息
        updateStatsInfo();
        
        // 设置懒加载
        this.setupImageLazyLoading();
        
        // 触发自定义事件
        const event = new CustomEvent('databasesRendered', {
            detail: { count: window.allDatabases.length }
        });
        document.dispatchEvent(event);
        
        console.log('✅ 性能优化渲染完成:', window.allDatabases.length, '个资源');
    }
    
    // 设置懒加载
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const card = entry.target;
                        // 懒加载卡片内容
                        this.loadCardContent(card);
                        observer.unobserve(card);
                    }
                });
            }, {
                rootMargin: `${this.lazyLoadOffset}px`
            });
            
            // 观察所有卡片
            document.addEventListener('databasesRendered', () => {
                document.querySelectorAll('.database-card').forEach(card => {
                    observer.observe(card);
                });
            });
        }
    }
    
    // 加载卡片内容
    loadCardContent(card) {
        // 这里可以添加更多懒加载逻辑
        // 例如：懒加载图片、延迟加载工具提示等
        card.classList.add('loaded');
    }
    
    // 优化搜索功能
    optimizeSearch() {
        const originalHandleSearch = window.handleSearch;
        
        window.handleSearch = this.debounce(() => {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
            
            if (searchTerm.length === 0) {
                window.filteredDatabases = [...window.allDatabases];
            } else {
                // 使用预计算的搜索文本
                window.filteredDatabases = window.allDatabases.filter(db => 
                    db._searchText.includes(searchTerm)
                );
            }
            
            // 批量重新渲染
            this.renderInBatches(window.filteredDatabases);
            
        }, this.debounceDelay);
    }
    
    // 设置虚拟滚动（对于大量数据）
    setupVirtualScrolling() {
        // 如果数据量超过500个，启用虚拟滚动
        if (window.allDatabases && window.allDatabases.length > 500) {
            console.log('🚀 启用虚拟滚动优化');
            // 这里可以实现虚拟滚动逻辑
        }
    }
    
    // 预加载关键资源
    preloadCriticalResources() {
        // 预加载字体
        const fontLink = document.createElement('link');
        fontLink.rel = 'preload';
        fontLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
        fontLink.as = 'style';
        document.head.appendChild(fontLink);
        
        // 预连接到外部域名
        const preconnectLinks = [
            'https://cdnjs.cloudflare.com',
            'https://fonts.googleapis.com',
            'https://www.google-analytics.com'
        ];
        
        preconnectLinks.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preconnect';
            link.href = url;
            document.head.appendChild(link);
        });
    }
    
    // 图片懒加载
    setupImageLazyLoading() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            images.forEach(img => imageObserver.observe(img));
        } else {
            // 降级处理
            images.forEach(img => {
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
            });
        }
    }
    
    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // 性能监控
    monitorPerformance() {
        if ('performance' in window) {
            window.addEventListener('load', () => {
                setTimeout(() => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    console.log('📊 页面性能数据:', {
                        loadTime: Math.round(perfData.loadEventEnd - perfData.fetchStart),
                        domContentLoaded: Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart),
                        firstPaint: Math.round(performance.getEntriesByType('paint')[0]?.startTime || 0)
                    });
                }, 0);
            });
        }
    }
}

// 添加CSS优化
const optimizedCSS = `
    <style>
        /* 性能优化样式 */
        .database-card {
            contain: content;
            will-change: transform;
        }
        
        .database-card.loaded {
            animation: fadeInUp 0.3s ease;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .loading-optimized .spinner {
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* 优化滚动性能 */
        .databases-grid {
            contain: layout;
        }
        
        /* 减少重绘 */
        .btn {
            backface-visibility: hidden;
            transform: translateZ(0);
        }
    </style>
`;

document.head.insertAdjacentHTML('beforeend', optimizedCSS);

// 页面加载完成后初始化性能优化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.performanceOptimizer = new PerformanceOptimizer();
    });
} else {
    window.performanceOptimizer = new PerformanceOptimizer();
}

// 导出类
window.PerformanceOptimizer = PerformanceOptimizer;
