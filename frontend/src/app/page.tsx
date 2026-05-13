import React from "react";
import Image from "next/image";
import Header from "@/componenets/Header/Header";
import "./home.css";
import Footer from "@/componenets/Footer/Footer";

const page: React.FC = () => {
  const uniquePoints = [
    {
      img: "/unique1.png",
      title: "Not Just an AI Wrapper",
      description:
        "Our system retrieves relevant legal sources before generating responses — ensuring grounded and context-aware outputs. ",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        </svg>
      ),
    },
    {
      img: "unique2.png",
      title: "Powered by Retrieval-Augmented Generation (RAG)",
      description:
        "Instead of generating answers purely from model memory, the system first retrieves relevant legal materials and then generates responses based on that context. This retrieval-first approach improves precision, contextual relevance, and legal reliability.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 6v6l4 2" />
        </svg>
      ),
    },
    {
      img: "unique3.png",
      title: "Grounded in Actual Legal Documents",
      description:
        "Every response is grounded in retrieved legal sources — such as statutes, case law, and contractual text — reducing hallucination risk and increasing trustworthiness for professional legal use.",
      icon: (
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="16" y1="13" x2="8" y2="13" />
          <line x1="16" y1="17" x2="8" y2="17" />
          <polyline points="10 9 9 9 8 9" />
        </svg>
      ),
    },
  ];

  const features = [
    {
      title: "Client & Appointment Management",
      description:
        "Manage clients and appointments efficiently with an integrated system. Add, edit, and organize appointments while keeping your legal workflow streamlined in one platform.",
      image: "/feature1.png",
      alt: "Client management dashboard showing appointment scheduling interface",
    },
    {
      title: "Legal Research Intelligence",
      description:
        "Powered by Retrieval-Augmented Generation (RAG), our system retrieves relevant statutes, case laws, and legal provisions before generating responses — ensuring accurate and grounded legal insights.",
      image: "/feature2.png",
      alt: "Legal research interface with AI-powered analysis results",
    },
    {
      title: "Clause Analysis & Review",
      description:
        "Paste or upload contract clauses and receive structured explanations, risk identification, and legal implications — simplifying complex legal language into clear insights.",
      image: "/feature3.png",
      alt: "Contract clause analysis tool showing structured legal review",
    },
  ];

  return (
    <main>
      <Header />

      {/* ── Hero Section ──────────────────────────── */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-rule" />
          <h1>Accelerate Your Legal Research.</h1>
          <p className="hero-subtitle">
            AI Legal Assistant helps you find relevant laws and review contracts
            quickly — saving time without sacrificing accuracy.
          </p>

          <div className="hero-actions">
            <a href="/legal" className="hero-btn-primary">
              Start Researching
            </a>
            <a href="/contract" className="hero-btn-secondary">
              Analyze a Clause
            </a>
          </div>

          {/* Trust bar */}
          <div className="trust-bar">
            <div className="trust-item">
              <span className="trust-check">✓</span>
              RAG-powered accuracy
            </div>
            <div className="trust-item">
              <span className="trust-check">✓</span>
              BNS &amp; Contract Law covered
            </div>
            <div className="trust-item">
              <span className="trust-check">✓</span>
              PDF export ready
            </div>
          </div>
        </div>

        <div className="hero-banner">
          <div className="hero-image-frame">
            <Image
              src="/banner.png"
              alt="AI Legal Assistant platform overview showing legal research and analysis tools"
              width={700}
              height={500}
              priority
              sizes="(max-width: 1100px) 100vw, 50vw"
            />
          </div>
        </div>
      </section>

      {/* ── Features Section ──────────────────────── */}
      <section className="home-feature">
        <h2 className="feature-title">Tailored for Legal Professionals</h2>

        {features.map((feature, index) => (
          <section
            className={`feature-row ${index % 2 !== 0 ? "feature-row-reverse" : ""}`}
            key={feature.title}
          >
            <div className="feature-image">
              <div className="feature-image-card">
                <Image
                  src={feature.image}
                  alt={feature.alt}
                  width={500}
                  height={350}
                  loading="lazy"
                  sizes="(max-width: 1100px) 100vw, 50vw"
                />
              </div>
            </div>
            <div className="feature-text">
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          </section>
        ))}

        {/* ── How It Works Section ────────────────── */}
        <section className="how-it-works">
          <h2 className="feature-title">How It Works</h2>
          <div className="steps-container">
            <div className="step-card">
              <div className="step-number">01</div>
              <h4>Upload or Search</h4>
              <p>Input your legal query or upload a contract clause for analysis.</p>
            </div>
            <div className="step-card">
              <div className="step-number">02</div>
              <h4>RAG Processing</h4>
              <p>Our system retrieves relevant statutes and case laws from our database.</p>
            </div>
            <div className="step-card">
              <div className="step-number">03</div>
              <h4>Expert Generation</h4>
              <p>Gemini AI generates a grounded, context-aware legal insight.</p>
            </div>
          </div>
        </section>

        {/* ── Unique Value Section ─────────────────── */}
        <section className="unique-section">
          <h2>Why Professionals Choose Us</h2>

          <div className="unique-grid">
            {uniquePoints.map((point) => (
              <div className="unique-card" key={point.title}>
                <div className="unique-card-accent" />
                <div className="unique-icon-area">
                  {point.icon}
                </div>
                <h3>{point.title}</h3>
                <p>{point.description}</p>
              </div>
            ))}
          </div>
        </section>
      </section>
      <Footer />
    </main>
  );
};

export default page;
