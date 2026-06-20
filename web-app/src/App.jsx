import React, { useState } from 'react';
import { Search, PenTool, Globe, TrendingUp, ShoppingBag, Sparkles, Send, ChevronDown, ChevronUp, Loader2, BarChart3, Database } from 'lucide-react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = "http://localhost:8000";

function ProductCard({ product, index }) {
  const [loading, setLoading] = useState(false);
  const [blogData, setBlogData] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [pubStatus, setPubStatus] = useState("");

  const generateBlog = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/generate-blog`, {
        product_title: product.title
      });
      setBlogData(res.data);
      setExpanded(true);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const publishBlog = async (platform) => {
    if (!blogData) return;
    setPublishing(true);
    setPubStatus(`Publishing to ${platform}...`);
    try {
      const res = await axios.post(`${API_BASE}/publish`, {
        title: blogData.title,
        content: blogData.content,
        platform: platform
      });
      if (res.data.status === "success") {
        setPubStatus(`✅ Published to ${platform}!`);
        window.open(res.data.url, '_blank');
      } else {
        setPubStatus(`⚠️ ${res.data.reason || res.data.message}`);
      }
    } catch (err) {
      setPubStatus("❌ Publishing failed.");
    }
    setPublishing(false);
  };

  const [showModal, setShowModal] = useState(false);

  const downloadReport = () => {
    if (!blogData) return;
    const header = `SEO STRATEGY REPORT: ${product.title}\n${'='.repeat(40)}\n\n`;
    const body = blogData.keywords.map(k => {
      const isObject = typeof k === 'object' && k !== null;
      return `KEYWORD: #${isObject ? k.keyword : k}\nINTENT: ${isObject ? k.intent : 'N/A'}\nCOMPETITION: ${isObject ? k.competition : 'N/A'}\nSTRATEGY: ${isObject ? k.strategy : 'N/A'}\n${'-'.repeat(20)}`;
    }).join('\n\n');
    
    const blob = new Blob([header + body], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${product.title.slice(0, 20)}_SEO_Report.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="glass-card"
      style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.25rem', position: 'relative' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ background: 'rgba(139, 92, 246, 0.1)', padding: '0.6rem', borderRadius: '0.75rem' }}>
          <ShoppingBag size={20} color="#8b5cf6" />
        </div>
        <span className="status-badge">
          <Sparkles size={12} /> eBay Trending
        </span>
      </div>

      <div>
        <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem', fontWeight: '700', color: '#f1f5f9', lineHeight: '1.4' }}>
          {product.title}
        </h3>
        <p style={{ color: '#ec4899', fontWeight: '800', fontSize: '1.3rem', margin: 0 }}>
          {product.price}
        </p>
      </div>

      {!blogData ? (
        <button
          onClick={generateBlog}
          className="btn-primary"
          disabled={loading}
        >
          {loading ? (
            <><Loader2 size={18} className="spin-icon" /> Creating Magic...</>
          ) : (
            <><PenTool size={18} /> Generate Blog Post</>
          )}
        </button>
      ) : (
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button
            onClick={() => setExpanded(!expanded)}
            className="btn-primary"
            style={{ flex: 2, background: 'linear-gradient(135deg, #10b981, #059669)', boxShadow: '0 4px 15px rgba(16, 185, 129, 0.3)' }}
          >
            {expanded ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
            {expanded ? "Collapse Preview" : "View Blog"}
          </button>
          <button
            onClick={() => setShowModal(true)}
            className="btn-primary"
            style={{ flex: 1, background: 'rgba(139, 92, 246, 0.1)', border: '1px solid var(--primary)', color: 'var(--primary)', boxShadow: 'none' }}
            title="View SEO Report"
          >
            <BarChart3 size={18} />
          </button>
        </div>
      )}

      <AnimatePresence>
        {blogData && expanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            style={{ overflow: 'hidden' }}
          >
            <div style={{ padding: '1rem 0' }}>
              <div style={{ marginBottom: '1.25rem' }}>
                <h4 style={{ color: '#94a3b8', marginBottom: '0.75rem', fontSize: '0.8rem', textTransform: 'uppercase', letterSpacing: '0.05em', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <PenTool size={14} /> Blog Content Preview
                </h4>
              </div>

              <div className="blog-preview-container">
                <div className="blog-text" style={{ maxHeight: '350px', overflowY: 'auto', paddingRight: '0.5rem' }}>
                  <div dangerouslySetInnerHTML={{ __html: blogData?.content?.replace(/\n/g, '<br/>') }} />
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.25rem' }}>
                <button
                  onClick={() => publishBlog('wordpress')}
                  className="btn-primary"
                  style={{ flex: 1, padding: '0.6rem', fontSize: '0.8rem' }}
                  disabled={publishing}
                >
                  <Globe size={16} /> WordPress
                </button>
                <button
                  onClick={() => publishBlog('medium')}
                  className="btn-primary"
                  style={{ flex: 1, padding: '0.6rem', fontSize: '0.8rem', background: 'linear-gradient(135deg, #475569, #1e293b)' }}
                  disabled={publishing}
                >
                  <Send size={16} /> Medium
                </button>
              </div>
              
              {pubStatus && (
                <motion.p 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  style={{ fontSize: '0.75rem', color: '#818cf8', textAlign: 'center', marginTop: '0.75rem', fontWeight: '600' }}
                >
                  {pubStatus}
                </motion.p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* SEO Report Modal */}
      <AnimatePresence>
        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <motion.div 
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="modal-content glass-card"
              onClick={e => e.stopPropagation()}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h2 style={{ margin: 0, fontSize: '1.5rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <BarChart3 size={28} color="#c084fc" /> SEO Strategy Report
                </h2>
                <button onClick={() => setShowModal(false)} className="close-btn">&times;</button>
              </div>

              <div className="report-grid">
                {blogData?.keywords?.map((k, i) => {
                  const isObject = typeof k === 'object' && k !== null;
                  const keyword = isObject ? k.keyword : k;
                  const intent = isObject ? k.intent : 'N/A';
                  const competition = isObject ? k.competition : 'N/A';
                  const strategy = isObject ? k.strategy : 'Optimization strategy pending.';

                  return (
                    <div key={i} className="keyword-report-card" style={{ background: 'rgba(255,255,255,0.03)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                        <span className="keyword-tag" style={{ fontSize: '1rem', background: 'rgba(139, 92, 246, 0.2)' }}>#{keyword}</span>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                          <span className="mini-badge" style={{ background: 'rgba(6, 182, 212, 0.1)', color: '#06b6d4', padding: '0.3rem 0.6rem' }}>{intent}</span>
                          <span className="mini-badge" style={{ 
                            background: competition?.toLowerCase().includes('low') ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                            color: competition?.toLowerCase().includes('low') ? '#10b981' : '#f87171',
                            padding: '0.3rem 0.6rem'
                          }}>{competition}</span>
                        </div>
                      </div>
                      <p style={{ margin: 0, fontSize: '0.9rem', color: '#cbd5e1', lineHeight: '1.6' }}>
                        <strong style={{ color: '#c084fc' }}>Execution Strategy:</strong> {strategy}
                      </p>
                    </div>
                  );
                })}
              </div>

              <div style={{ marginTop: '2.5rem', display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                <button className="btn-secondary" onClick={() => setShowModal(false)}>Close</button>
                <button className="btn-primary" onClick={downloadReport}>
                  <Database size={18} /> Download Full Report (.txt)
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function App() {
  const [products, setProducts] = useState([]);
  const [scraping, setScraping] = useState(false);
  const [status, setStatus] = useState("");

  const fetchTrending = async () => {
    setScraping(true);
    setStatus("🔍 Analyzing market trends and scraping data...");
    try {
      const res = await axios.get(`${API_BASE}/trending`);
      setProducts(res.data);
      setStatus(`✨ Success: Identified ${res.data.length} trending items!`);
    } catch (err) {
      console.error(err);
      setStatus("❌ Error: Analysis pipeline failed.");
    }
    setScraping(false);
  };

  return (
    <div className="container">
      <header style={{ marginBottom: '4rem', textAlign: 'center' }}>
        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '1.25rem', marginBottom: '1.5rem' }}>
            <div className="header-icon">
              <Sparkles size={32} color="white" />
            </div>
            <h1 style={{ fontSize: '3.5rem', margin: 0, fontWeight: '900', letterSpacing: '-0.04em', background: 'linear-gradient(to right, #ffffff, #a5b4fc)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              SEO Engine <span style={{ color: '#a855f7', WebkitTextFillColor: 'initial' }}>AI</span>
            </h1>
          </div>
          <p style={{ color: '#94a3b8', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto', lineHeight: '1.6' }}>
            Hyper-automate your content pipeline. Scrape trending high-margin products and generate rank-ready SEO blogs instantly.
          </p>
        </motion.div>
      </header>

      <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginBottom: '3.5rem' }}>
        <button 
          onClick={fetchTrending} 
          className="btn-primary" 
          disabled={scraping} 
          style={{ fontSize: '1.1rem', padding: '1rem 2.5rem', borderRadius: '1.25rem' }}
        >
          {scraping ? (
            <><Loader2 size={24} className="spin-icon" /> Processing Neural Data...</>
          ) : (
            <><Database size={22} /> Discover Trending Products</>
          )}
        </button>
      </div>

      {status && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          style={{ 
            textAlign: 'center', 
            marginBottom: '3rem', 
            color: '#c084fc', 
            fontWeight: '600',
            background: 'rgba(139, 92, 246, 0.1)',
            padding: '0.75rem 1.5rem',
            borderRadius: '2rem',
            width: 'fit-content',
            margin: '0 auto 3rem auto',
            border: '1px solid rgba(139, 92, 246, 0.2)'
          }}
        >
          {status}
        </motion.div>
      )}

      <div className="grid-products">
        <AnimatePresence>
          {products.map((p, idx) => (
            <ProductCard key={idx} product={p} index={idx} />
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
