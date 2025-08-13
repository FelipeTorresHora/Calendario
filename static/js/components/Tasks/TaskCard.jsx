import React, { useState } from 'react';
import { Draggable } from 'react-beautiful-dnd';
import './TaskCard.css';

const TaskCard = ({ task, index, onComplete, onEdit, onDelete, compact = false }) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleComplete = (e) => {
    e.stopPropagation();
    onComplete(task.id);
  };

  const handleEdit = (e) => {
    e.stopPropagation();
    onEdit && onEdit(task);
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      onDelete && onDelete(task.id);
    }
  };

  const CardContent = () => (
    <div 
      className={`task-card ${compact ? 'compact' : ''} ${task.is_done ? 'completed' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="task-content">
        <div className="task-checkbox">
          <input
            type="checkbox"
            checked={task.is_done}
            onChange={handleComplete}
            className="checkbox"
          />
        </div>
        
        <div className="task-text">
          <span className={task.is_done ? 'completed-text' : ''}>
            {task.description}
          </span>
          {!compact && (
            <div className="task-meta">
              {task.date && (
                <span className="task-date">
                  {new Date(task.date).toLocaleDateString('pt-BR')}
                </span>
              )}
            </div>
          )}
        </div>
      </div>
      
      {(isHovered || !compact) && (
        <div className="task-actions">
          {onEdit && (
            <button 
              onClick={handleEdit}
              className="action-btn edit-btn"
              title="Editar"
            >
              ✏️
            </button>
          )}
          {onDelete && (
            <button 
              onClick={handleDelete}
              className="action-btn delete-btn"
              title="Excluir"
            >
              🗑️
            </button>
          )}
        </div>
      )}
    </div>
  );

  // If draggable and not compact, wrap with Draggable
  if (!compact && index !== undefined) {
    return (
      <Draggable draggableId={`task-${task.id}`} index={index}>
        {(provided, snapshot) => (
          <div
            ref={provided.innerRef}
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            className={`draggable-task ${snapshot.isDragging ? 'dragging' : ''}`}
          >
            <CardContent />
          </div>
        )}
      </Draggable>
    );
  }

  return <CardContent />;
};

export default TaskCard;