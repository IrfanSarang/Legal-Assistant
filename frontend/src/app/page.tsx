import React from "react";
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
    },
    {
      img: "unique2.png",
      title: "Powered by Retrieval-Augmented Generation (RAG)",
      description:
        "Instead of generating answers purely from model memory, the system first retrieves relevant legal materials and then generates responses based on that context.This retrieval-first approach improves precision, contextual relevance, and legal reliability.",
    },
    {
      img: "unique3.png",
      title: "Grounded in Actual Legal Documents",
      description:
        "Every response is grounded in retrieved legal sources — such as statutes, case law, and contractual text — reducing hallucination risk and increasing trustworthiness for professional legal use.",
    },
  ];
  return (
    <main>
      <Header />
      <section className="hero">
        <div className="hero-content">
          <h1>Accelerate Your Legal Research.</h1>

          <p>
            AI Legal Assistant helps you find relevant laws and review contracts
            quickly — saving time without sacrificing accuracy.
          </p>
        </div>

        <div className="hero-banner">
          <img src="/banner.png" alt="AI Legal Assistant" />
        </div>
      </section>

      <section className="home-feature">
        <h1 className="feature-title">Features</h1>

        {/* Feature 1 */}
        <section className="feature-row">
          <div className="feature-text">
            <h3>Client & Appointment Management</h3>
            <p>
              Manage clients and appointments efficiently with an integrated
              system. Add, edit, and organize appointments while keeping your
              legal workflow streamlined in one platform.
            </p>
          </div>
          <div className="feature-image">
            <img src="/feature1.png" alt="Client Management" />
          </div>
        </section>

        {/* Feature 2 */}
        <section className="feature-row">
          <div className="feature-text">
            <h3>Legal Research Intelligence</h3>
            <p>
              Powered by Retrieval-Augmented Generation (RAG), our system
              retrieves relevant statutes, case laws, and legal provisions
              before generating responses — ensuring accurate and grounded legal
              insights.
            </p>
          </div>
          <div className="feature-image">
            <img src="/feature2.png" alt="Legal Research" />
          </div>
        </section>

        {/* Feature 3 */}
        <section className="feature-row">
          <div className="feature-text">
            <h3>Clause Analysis & Review</h3>
            <p>
              Paste or upload contract clauses and receive structured
              explanations, risk identification, and legal implications —
              simplifying complex legal language into clear insights.
            </p>
          </div>
          <div className="feature-image">
            <img src="/feature3.png" alt="Clause Analysis" />
          </div>
        </section>

        <section className="unique-section">
          <h2>Why It’s Unique</h2>

          <div className="unique-grid">
            {uniquePoints.map((point) => (
              <div className="unique-card" key={point.title}>
                <img src={point.img} alt={point.title} />
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
