// 修复筛选功能的脚本
// 确保分类筛选和类型筛选正常工作

(function() {
    'use strict';
    
    // 等待页面和数据加载完成
    function waitForData() {
        return new Promise((resolve) => {
            const checkData = () => {
                if (window.allDatabases && window.allDatabases.length > 0) {
                    resolve();
                } else {
                    setTimeout(checkData, 100);
                }
            };
            checkData();
        });
    }
    
    // 修复分类筛选器渲染
    function fixCategoryFilters() {
        console.log('🔧 修复分类筛选器...');
        
        const categoryIcons = {
            'protein': 'fas fa-atom',
            'genomics': 'fas fa-dna',
            'plant': 'fas fa-seedling',
            'medical': 'fas fa-heartbeat',
            'microbiology': 'fas fa-bacteria',
            'evolution': 'fas fa-project-diagram',
            'omics': 'fas fa-chart-line',
            'tools': 'fas fa-tools'
        };
        
        const categories = {};
        
        // 统计各分类数量
        window.allDatabases.forEach(db => {
            const category = db.category || 'unknown';
            if (!categories[category]) {
                categories[category] = {
                    name: db.category_name || category,
                    count: 0
                };
            }
            categories[category].count++;
        });
        
        console.log('📊 发现分类:', Object.keys(categories));
        
        // 生成分类筛选HTML
        const filtersHTML = Object.entries(categories).map(([key, value]) => `
            <li>
                <a href="#" class="category-filter" data-category="${key}">
                    <i class="${categoryIcons[key] || 'fas fa-folder'}"></i>
                    <span>${value.name}</span>
                    <span class="category-count">${value.count}</span>
                </a>
            </li>
        `).join('');
        
        // 更新分类筛选器
        const categoryFiltersContainer = document.getElementById('categoryFilters');
        if (categoryFiltersContainer) {
            // 保留"全部资源"项
            const allResourcesHTML = `
                <li>
                    <a href="#" class="category-filter active" data-category="all">
                        <i class="fas fa-globe"></i>
                        <span>全部资源</span>
                        <span class="category-count">${window.allDatabases.length}</span>
                    </a>
                </li>
            `;
            
            categoryFiltersContainer.innerHTML = allResourcesHTML + filtersHTML;
            console.log('✅ 分类筛选器已更新');
        }
    }
    
    // 修复事件监听器
    function fixEventListeners() {
        console.log('🔧 修复事件监听器...');
        
        // 分类筛选事件
        const categoryFiltersContainer = document.getElementById('categoryFilters');
        if (categoryFiltersContainer) {
            categoryFiltersContainer.addEventListener('click', function(e) {
                e.preventDefault();
                const filterLink = e.target.closest('.category-filter');
                if (filterLink) {
                    const category = filterLink.dataset.category;
                    console.log('🔍 分类筛选:', category);
                    
                    // 更新活跃状态
                    document.querySelectorAll('#categoryFilters .category-filter').forEach(f => 
                        f.classList.remove('active'));
                    filterLink.classList.add('active');
                    
                    // 更新全局变量
                    window.currentCategory = category;
                    
                    // 执行筛选
                    performFilter();
                }
            });
        }
        
        // 类型筛选事件
        const typeFiltersContainer = document.getElementById('typeFilters');
        if (typeFiltersContainer) {
            typeFiltersContainer.addEventListener('click', function(e) {
                e.preventDefault();
                const filterLink = e.target.closest('.category-filter');
                if (filterLink) {
                    const type = filterLink.dataset.type;
                    console.log('🔍 类型筛选:', type);
                    
                    // 更新活跃状态
                    document.querySelectorAll('#typeFilters .category-filter').forEach(f => 
                        f.classList.remove('active'));
                    filterLink.classList.add('active');
                    
                    // 更新全局变量
                    window.currentType = type;
                    
                    // 执行筛选
                    performFilter();
                }
            });
        }
        
        console.log('✅ 事件监听器已修复');
    }
    
    // 执行筛选
    function performFilter() {
        console.log('🔄 执行筛选...', {
            category: window.currentCategory,
            type: window.currentType,
            search: window.searchTerm
        });
        
        window.filteredDatabases = window.allDatabases.filter(db => {
            // 分类过滤
            const categoryMatch = window.currentCategory === 'all' || 
                                 db.category === window.currentCategory;
            
            // 类型过滤
            const resourceType = db.resource_type || 'database';
            const typeMatch = window.currentType === 'all' || 
                             (window.currentType === 'database' && resourceType === 'database') ||
                             (window.currentType === 'web' && resourceType === 'web');
            
            // 搜索过滤
            const searchTerm = window.searchTerm || '';
            const searchMatch = !searchTerm || 
                               (db.name && db.name.toLowerCase().includes(searchTerm)) ||
                               (db.short_description && db.short_description.toLowerCase().includes(searchTerm)) ||
                               (db.short_description_zh && db.short_description_zh.includes(searchTerm));
            
            return categoryMatch && typeMatch && searchMatch;
        });
        
        console.log('📊 筛选结果:', window.filteredDatabases.length, '个资源');
        
        // 重新渲染
        if (typeof renderDatabases === 'function') {
            renderDatabases();
        } else if (window.performanceOptimizer && typeof window.performanceOptimizer.renderInBatches === 'function') {
            window.performanceOptimizer.renderInBatches(window.filteredDatabases);
        }
    }
    
    // 初始化修复
    async function initFix() {
        console.log('🚀 开始修复筛选功能...');
        
        // 等待数据加载
        await waitForData();
        console.log('✅ 数据已加载:', window.allDatabases.length, '个资源');
        
        // 初始化全局变量
        window.currentCategory = window.currentCategory || 'all';
        window.currentType = window.currentType || 'all';
        window.searchTerm = window.searchTerm || '';
        window.filteredDatabases = window.filteredDatabases || [...window.allDatabases];
        
        // 修复分类筛选器
        fixCategoryFilters();
        
        // 修复事件监听器
        fixEventListeners();
        
        console.log('🎉 筛选功能修复完成！');
    }
    
    // 页面加载完成后执行修复
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initFix);
    } else {
        initFix();
    }
    
})();
