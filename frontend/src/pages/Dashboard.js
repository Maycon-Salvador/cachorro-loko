import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Dashboard() {
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSubscription = async () => {
      try {
        const response = await api.get("/api/subscription/");
        setSubscription(response.data);
      } catch (err) {
        console.error(err);
        localStorage.clear();
        navigate("/login");
      } finally {
        setLoading(false);
      }
    };
    fetchSubscription();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (loading) return <p>Carregando...</p>;

  return (
    <div
      style={{
        maxWidth: 600,
        margin: "50px auto",
        padding: 20,
        border: "1px solid #ddd",
        borderRadius: 8,
      }}
    >
      <h2>Minha Assinatura - Cachorro Loko</h2>
      <button
        onClick={handleLogout}
        style={{
          marginBottom: 20,
          padding: 8,
          background: "#dc3545",
          color: "#fff",
          border: "none",
          borderRadius: 4,
        }}
      >
        Sair
      </button>

      {subscription && subscription.status === "none" ? (
        <p>Você ainda não possui assinatura ativa.</p>
      ) : subscription ? (
        <div>
          <p>
            <strong>Status:</strong>{" "}
            {subscription.status === "active" ? "✅ Em dia" : "❌ Vencida"}
          </p>
          <p>
            <strong>Vencimento:</strong> {subscription.next_due_date}
          </p>
          <p>
            <strong>Dias restantes:</strong>{" "}
            {subscription.days_remaining >= 0
              ? subscription.days_remaining
              : "Vencido"}
          </p>
          <p>
            <strong>Valor mensal:</strong> R${" "}
            {(subscription.amount_cents / 100).toFixed(2)}
          </p>
        </div>
      ) : null}
    </div>
  );
}

export default Dashboard;
