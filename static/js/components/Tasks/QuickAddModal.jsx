import React, { useState, useEffect } from 'react';
import { format } from 'date-fns';
import './QuickAddModal.css';

const QuickAddModal = ({ selectedDate, onSave, onClose }) => {
  const [description, setDescription] = useState('');
  const [date, setDate] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (selectedDate) {
      setDate(format(selectedDate, 'yyyy-MM-dd'));
    }
  }, [selectedDate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!description.trim()) {
      alert('Por favor, digite uma descrição para a tarefa');
      return;
    }

    setIsLoading(true);
    
    try {
      await onSave({
        description: description.trim(),
        date: date,
      });
      
      // Reset form
      setDescription('');
      setDate('');
    } catch (error) {
      console.error('Erro ao salvar tarefa:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" onClick={handleBackdropClick}>
      <div className="quick-add-modal">
        <div className="modal-header">
          <h3>Nova Tarefa</h3>
          <button 
            className="close-btn"
            onClick={onClose}
            type="button"
          >
            ×
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="modal-form">
          <div className="form-group">
            <label htmlFor="task-description">Descrição:</label>
            <textarea
              id="task-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Digite a descrição da tarefa..."
              rows={3}
              className="form-textarea"
              autoFocus
              disabled={isLoading}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="task-date">Data:</label>
            <input
              id="task-date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="form-input"
              disabled={isLoading}
              required
            />
          </div>
          
          <div className="modal-actions">
            <button 
              type="button" 
              onClick={onClose}
              className="btn btn-secondary"
              disabled={isLoading}
            >
              Cancelar
            </button>
            <button 
              type="submit"
              className="btn btn-primary"
              disabled={isLoading || !description.trim()}
            >
              {isLoading ? 'Salvando...' : 'Salvar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default QuickAddModal;