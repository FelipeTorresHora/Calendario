import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import TaskCard from './TaskCard';
import { apiRequest, showToast } from '../../utils/django';
import './TaskList.css';

const TaskList = ({ tasks: initialTasks, csrfToken }) => {
  const [tasks, setTasks] = useState(initialTasks || []);
  const [filter, setFilter] = useState('all'); // all, pending, completed
  const [sortBy, setSortBy] = useState('date'); // date, priority, created

  // Filter and sort tasks
  const filteredTasks = tasks
    .filter(task => {
      if (filter === 'pending') return !task.is_done;
      if (filter === 'completed') return task.is_done;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'date') {
        return new Date(a.date) - new Date(b.date);
      }
      if (sortBy === 'created') {
        return b.id - a.id; // Newer first
      }
      return 0;
    });

  // Handle task completion
  const handleTaskComplete = async (taskId) => {
    try {
      await apiRequest(`/tasks/${taskId}/complete/`, {
        method: 'POST',
      });
      
      setTasks(prevTasks => 
        prevTasks.map(task => 
          task.id === taskId ? { ...task, is_done: !task.is_done } : task
        )
      );
      
      showToast('Tarefa atualizada!', 'success');
    } catch (error) {
      showToast('Erro ao atualizar tarefa', 'error');
    }
  };

  // Handle task deletion
  const handleTaskDelete = async (taskId) => {
    try {
      await apiRequest(`/tasks/${taskId}/delete/`, {
        method: 'DELETE',
      });
      
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      showToast('Tarefa excluída!', 'success');
    } catch (error) {
      showToast('Erro ao excluir tarefa', 'error');
    }
  };

  // Handle task edit (placeholder)
  const handleTaskEdit = (task) => {
    // For now, just show an alert - could open a modal
    alert(`Editar tarefa: ${task.description}`);
  };

  // Handle drag end
  const handleDragEnd = async (result) => {
    if (!result.destination) return;

    const items = Array.from(filteredTasks);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    // Update local state immediately for better UX
    setTasks(items);

    // TODO: Send reorder request to backend if needed
    showToast('Tarefa reordenada!', 'info');
  };

  const getFilterStats = () => {
    const total = tasks.length;
    const completed = tasks.filter(t => t.is_done).length;
    const pending = total - completed;
    
    return { total, completed, pending };
  };

  const stats = getFilterStats();

  return (
    <div className="task-list-container">
      {/* Header */}
      <div className="task-list-header">
        <h3>Minhas Tarefas</h3>
        <div className="task-stats">
          <span className="stat">
            Total: <strong>{stats.total}</strong>
          </span>
          <span className="stat">
            Pendentes: <strong>{stats.pending}</strong>
          </span>
          <span className="stat">
            Concluídas: <strong>{stats.completed}</strong>
          </span>
        </div>
      </div>

      {/* Filters */}
      <div className="task-filters">
        <div className="filter-group">
          <label>Filtrar:</label>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">Todas</option>
            <option value="pending">Pendentes</option>
            <option value="completed">Concluídas</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label>Ordenar:</label>
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            className="filter-select"
          >
            <option value="date">Data</option>
            <option value="created">Criação</option>
          </select>
        </div>
      </div>

      {/* Task List */}
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="task-list">
          {(provided, snapshot) => (
            <div
              {...provided.droppableProps}
              ref={provided.innerRef}
              className={`task-list ${snapshot.isDraggingOver ? 'drag-over' : ''}`}
            >
              {filteredTasks.length === 0 ? (
                <div className="empty-state">
                  <p>
                    {filter === 'all' 
                      ? 'Nenhuma tarefa encontrada'
                      : filter === 'pending' 
                      ? 'Nenhuma tarefa pendente'
                      : 'Nenhuma tarefa concluída'
                    }
                  </p>
                </div>
              ) : (
                filteredTasks.map((task, index) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    index={index}
                    onComplete={handleTaskComplete}
                    onEdit={handleTaskEdit}
                    onDelete={handleTaskDelete}
                  />
                ))
              )}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
};

export default TaskList;