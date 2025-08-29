// 社交媒体分享功能
// 为生物信息导航页面添加分享功能

class SocialSharing {
    constructor() {
        this.baseUrl = 'https://gausshuang.github.io/bioinfo123/';
        this.title = '生物信息资源导航 - NAR 2024-2025 | 893个精选生物信息资源';
        this.description = '专业的生物信息资源导航平台，收录NAR 2024-2025中893个重要生物信息资源，包含475个数据库和418个Web工具';
        this.hashtags = 'bioinformatics,database,NAR,生物信息学,数据库导航';
        
        this.initSharing();
    }
    
    // 初始化分享功能
    initSharing() {
        this.addShareButtons();
        this.addShareEvents();
    }
    
    // 添加分享按钮到页面
    addShareButtons() {
        const shareHTML = `
            <div class="social-share" style="
                position: fixed;
                right: 20px;
                top: 50%;
                transform: translateY(-50%);
                z-index: 1000;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                padding: 10px;
                display: flex;
                flex-direction: column;
                gap: 8px;
            ">
                <div style="text-align: center; font-size: 12px; color: #666; margin-bottom: 5px;">分享</div>
                
                <button class="share-btn" data-platform="wechat" title="分享到微信" style="
                    background: #1AAD19;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fab fa-weixin"></i>
                </button>
                
                <button class="share-btn" data-platform="weibo" title="分享到微博" style="
                    background: #E6162D;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fab fa-weibo"></i>
                </button>
                
                <button class="share-btn" data-platform="twitter" title="分享到Twitter" style="
                    background: #1DA1F2;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fab fa-twitter"></i>
                </button>
                
                <button class="share-btn" data-platform="linkedin" title="分享到LinkedIn" style="
                    background: #0077B5;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fab fa-linkedin-in"></i>
                </button>
                
                <button class="share-btn" data-platform="email" title="邮件分享" style="
                    background: #666;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fas fa-envelope"></i>
                </button>
                
                <button class="share-btn" data-platform="copy" title="复制链接" style="
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    width: 40px;
                    height: 40px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <i class="fas fa-link"></i>
                </button>
            </div>
            
            <!-- 响应式隐藏 -->
            <style>
                @media (max-width: 768px) {
                    .social-share {
                        display: none !important;
                    }
                }
            </style>
        `;
        
        document.body.insertAdjacentHTML('beforeend', shareHTML);
    }
    
    // 添加分享事件监听
    addShareEvents() {
        document.addEventListener('click', (e) => {
            const shareBtn = e.target.closest('.share-btn');
            if (shareBtn) {
                const platform = shareBtn.dataset.platform;
                this.share(platform);
            }
        });
    }
    
    // 执行分享
    share(platform) {
        const url = encodeURIComponent(this.baseUrl);
        const title = encodeURIComponent(this.title);
        const description = encodeURIComponent(this.description);
        const hashtags = encodeURIComponent(this.hashtags);
        
        let shareUrl = '';
        
        switch (platform) {
            case 'wechat':
                // 微信分享需要生成二维码
                this.showWeChatQR();
                break;
                
            case 'weibo':
                shareUrl = `https://service.weibo.com/share/share.php?url=${url}&title=${title}&pic=`;
                break;
                
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}&hashtags=${hashtags}`;
                break;
                
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}&title=${title}&summary=${description}`;
                break;
                
            case 'email':
                shareUrl = `mailto:?subject=${title}&body=${description}%0A%0A${url}`;
                break;
                
            case 'copy':
                this.copyToClipboard();
                return;
        }
        
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
        
        // 发送分析事件
        if (typeof gtag !== 'undefined') {
            gtag('event', 'social_share', {
                event_category: 'Social',
                event_label: platform,
                value: 1
            });
        }
    }
    
    // 显示微信二维码
    showWeChatQR() {
        // 创建二维码模态框
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        
        modal.innerHTML = `
            <div style="
                background: white;
                border-radius: 10px;
                padding: 30px;
                text-align: center;
                max-width: 300px;
            ">
                <h3 style="margin-bottom: 20px; color: #333;">微信扫码分享</h3>
                <div id="wechat-qr" style="margin-bottom: 20px;"></div>
                <p style="color: #666; font-size: 14px; margin-bottom: 20px;">
                    使用微信扫描二维码分享给好友
                </p>
                <button onclick="this.closest('[style*=\"position: fixed\"]').remove()" style="
                    background: #1AAD19;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 10px 20px;
                    cursor: pointer;
                ">关闭</button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // 生成二维码（使用在线API）
        const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(this.baseUrl)}`;
        const qrImg = document.createElement('img');
        qrImg.src = qrUrl;
        qrImg.style.cssText = 'width: 200px; height: 200px; border: 1px solid #ddd;';
        document.getElementById('wechat-qr').appendChild(qrImg);
        
        // 点击背景关闭
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });
    }
    
    // 复制链接到剪贴板
    async copyToClipboard() {
        try {
            await navigator.clipboard.writeText(this.baseUrl);
            this.showToast('链接已复制到剪贴板！', 'success');
        } catch (err) {
            // 降级方案
            const textArea = document.createElement('textarea');
            textArea.value = this.baseUrl;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('链接已复制到剪贴板！', 'success');
        }
    }
    
    // 显示提示消息
    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : '#007bff'};
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            z-index: 10001;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            animation: slideInRight 0.3s ease;
        `;
        
        toast.textContent = message;
        document.body.appendChild(toast);
        
        // 添加动画样式
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        // 3秒后移除
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new SocialSharing();
    });
} else {
    new SocialSharing();
}

// 导出类供其他脚本使用
window.SocialSharing = SocialSharing;

