import React, { useState, useEffect } from 'react';
import './MetricsChart.css';

const MetricsChart = ({ data }) => {
  const [animatedValues, setAnimatedValues] = useState({
    completionRate: 0,
    totalTasks: 0,
    completedTasks: 0
  });

  // Animate numbers on mount
  useEffect(() => {
    const animate = () => {
      const duration = 1000; // 1 second
      const steps = 60; // 60fps
      const increment = duration / steps;
      
      let currentStep = 0;
      
      const timer = setInterval(() => {
        currentStep++;
        const progress = currentStep / steps;
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        
        setAnimatedValues({
          completionRate: Math.floor(data.completion_rate * easeOutQuart),
          totalTasks: Math.floor(data.total_tasks * easeOutQuart),
          completedTasks: Math.floor(data.completed_tasks * easeOutQuart)
        });
        
        if (currentStep >= steps) {
          clearInterval(timer);
          setAnimatedValues({
            completionRate: data.completion_rate,
            totalTasks: data.total_tasks,
            completedTasks: data.completed_tasks
          });
        }
      }, increment);
    };
    
    if (data) {
      animate();
    }
  }, [data]);

  if (!data) {
    return (
      <div className="metrics-loading">
        <p>Carregando métricas...</p>
      </div>
    );
  }

  return (
    <div className="metrics-chart">
      <h3>Estatísticas de Produtividade</h3>
      
      <div className="metrics-grid">
        {/* Completion Rate Circle */}
        <div className="metric-card completion-rate">
          <div className="circular-progress">
            <svg className="progress-ring" width="120" height="120">
              <circle
                className="progress-ring-background"
                stroke="#e5e7eb"
                strokeWidth="8"
                fill="transparent"
                r="52"
                cx="60"
                cy="60"
              />
              <circle
                className="progress-ring-progress"
                stroke="#3b82f6"
                strokeWidth="8"
                fill="transparent"
                r="52"
                cx="60"
                cy="60"
                strokeDasharray={`${(animatedValues.completionRate / 100) * 326.73} 326.73`}
              />
            </svg>
            <div className="progress-text">
              <span className="percentage">{animatedValues.completionRate}%</span>
              <span className="label">Concluídas</span>
            </div>
          </div>
        </div>

        {/* Total Tasks */}
        <div className="metric-card">
          <div className="metric-icon">📝</div>
          <div className="metric-value">{animatedValues.totalTasks}</div>
          <div className="metric-label">Total de Tarefas</div>
        </div>

        {/* Completed Tasks */}
        <div className="metric-card">
          <div className="metric-icon">✅</div>
          <div className="metric-value">{animatedValues.completedTasks}</div>
          <div className="metric-label">Concluídas</div>
        </div>

        {/* Pending Tasks */}
        <div className="metric-card">
          <div className="metric-icon">⏳</div>
          <div className="metric-value">{data.total_tasks - data.completed_tasks}</div>
          <div className="metric-label">Pendentes</div>
        </div>
      </div>

      {/* Active Challenges */}
      {data.active_challenges_data && data.active_challenges_data.length > 0 && (
        <div className="challenges-section">
          <h4>Desafios Ativos</h4>
          <div className="challenges-list">
            {data.active_challenges_data.map((challenge, index) => (
              <div key={index} className="challenge-item">
                <div className="challenge-info">
                  <span className="challenge-title">{challenge.title}</span>
                  <span className="challenge-days">
                    {challenge.days_remaining} dias restantes
                  </span>
                </div>
                <div className="challenge-progress">
                  <div 
                    className="progress-bar"
                    style={{ width: `${challenge.completion_rate}%` }}
                  ></div>
                  <span className="progress-percentage">
                    {Math.round(challenge.completion_rate)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MetricsChart;