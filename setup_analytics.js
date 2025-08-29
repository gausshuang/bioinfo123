// Google Analytics 4 配置脚本
// 使用说明：将此代码添加到index.html的<head>标签中

const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX'; // 替换为实际的测量ID

// Google Analytics 4 配置
function setupGoogleAnalytics() {
    // 添加 gtag 脚本
    const gtagScript = document.createElement('script');
    gtagScript.async = true;
    gtagScript.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
    document.head.appendChild(gtagScript);
    
    // 初始化 gtag
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', GA_MEASUREMENT_ID, {
        // 增强电子商务跟踪（适用于资源点击）
        enhanced_ecommerce: true,
        // 自动跟踪外部链接
        link_attribution: true,
        // 跟踪文件下载
        file_download: true
    });
    
    // 自定义事件跟踪
    setupCustomTracking();
}

// 自定义事件跟踪
function setupCustomTracking() {
    // 跟踪数据库访问点击
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="http"]');
        if (link && link.classList.contains('btn-primary')) {
            const databaseName = link.closest('.database-card')?.querySelector('.database-name')?.textContent;
            const category = link.closest('.database-card')?.querySelector('.database-category')?.textContent;
            
            gtag('event', 'database_access', {
                event_category: 'Database',
                event_label: databaseName,
                custom_parameter_1: category,
                value: 1
            });
        }
    });
    
    // 跟踪搜索行为
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length > 2) {
                    gtag('event', 'search', {
                        event_category: 'Search',
                        event_label: this.value,
                        value: this.value.length
                    });
                }
            }, 1000);
        });
    }
    
    // 跟踪分类筛选
    document.addEventListener('click', function(e) {
        if (e.target.closest('.category-filter')) {
            const category = e.target.closest('.category-filter').dataset.category;
            const categoryName = e.target.closest('.category-filter').querySelector('span').textContent;
            
            gtag('event', 'category_filter', {
                event_category: 'Filter',
                event_label: categoryName,
                custom_parameter_1: category,
                value: 1
            });
        }
    });
    
    // 跟踪收藏行为
    window.toggleFavorite = function(dbId) {
        const originalToggleFavorite = window.toggleFavorite;
        
        // 执行原始收藏逻辑
        originalToggleFavorite.call(this, dbId);
        
        // 发送分析事件
        gtag('event', 'favorite_toggle', {
            event_category: 'User Interaction',
            event_label: dbId,
            value: 1
        });
    };
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupGoogleAnalytics);
} else {
    setupGoogleAnalytics();
}

// 导出配置用于手动集成
window.BioinfoNavAnalytics = {
    setup: setupGoogleAnalytics,
    measurementId: GA_MEASUREMENT_ID
};
