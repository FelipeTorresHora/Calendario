import React, { useState, useEffect } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay, isToday, isSameMonth } from 'date-fns';
import { ptBR } from 'date-fns/locale';
import TaskCard from '../Tasks/TaskCard';
import QuickAddModal from '../Tasks/QuickAddModal';
import { apiRequest, showToast } from '../../utils/django';
import './Calendar.css';

const Calendar = ({ tasks: initialTasks, userId, csrfToken }) => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [tasks, setTasks] = useState(initialTasks || []);
  const [selectedDate, setSelectedDate] = useState(null);
  const [showQuickAdd, setShowQuickAdd] = useState(false);
  const [view, setView] = useState('month'); // month, week, day

  // Generate calendar days
  const monthStart = startOfMonth(currentDate);
  const monthEnd = endOfMonth(currentDate);
  const days = eachDayOfInterval({ start: monthStart, end: monthEnd });

  // Get tasks for a specific day
  const getTasksForDay = (day) => {
    return tasks.filter(task => {
      const taskDate = new Date(task.date);
      return isSameDay(taskDate, day);
    });
  };

  // Handle task completion
  const handleTaskComplete = async (taskId) => {
    try {
      await apiRequest(`/tasks/${taskId}/complete/`, {
        method: 'POST',
      });
      
      setTasks(prevTasks => 
        prevTasks.map(task => 
          task.id === taskId ? { ...task, is_done: true } : task
        )
      );
      
      showToast('Tarefa concluída!', 'success');
    } catch (error) {
      showToast('Erro ao completar tarefa', 'error');
    }
  };

  // Handle quick add task
  const handleQuickAdd = async (taskData) => {
    try {
      const response = await apiRequest('/tasks/create/', {
        method: 'POST',
        body: JSON.stringify({
          description: taskData.description,
          date: taskData.date,
        }),
      });
      
      // Add new task to state
      setTasks(prevTasks => [...prevTasks, response.task]);
      setShowQuickAdd(false);
      showToast('Tarefa criada!', 'success');
    } catch (error) {
      showToast('Erro ao criar tarefa', 'error');
    }
  };

  // Handle date click
  const handleDateClick = (day) => {
    setSelectedDate(day);
    setShowQuickAdd(true);
  };

  // Navigation
  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  return (
    <div className="react-calendar">
      {/* Calendar Header */}
      <div className="calendar-header">
        <div className="calendar-nav">
          <button onClick={goToPreviousMonth} className="nav-btn">
            ←
          </button>
          <h2 className="current-month">
            {format(currentDate, 'MMMM yyyy', { locale: ptBR })}
          </h2>
          <button onClick={goToNextMonth} className="nav-btn">
            →
          </button>
        </div>
        
        <div className="calendar-actions">
          <button onClick={goToToday} className="today-btn">
            Hoje
          </button>
          <div className="view-switcher">
            <button 
              className={view === 'month' ? 'active' : ''} 
              onClick={() => setView('month')}
            >
              Mês
            </button>
            <button 
              className={view === 'week' ? 'active' : ''} 
              onClick={() => setView('week')}
            >
              Semana
            </button>
          </div>
        </div>
      </div>

      {/* Calendar Grid */}
      <div className="calendar-grid">
        {/* Weekday Headers */}
        {['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map(day => (
          <div key={day} className="weekday-header">
            {day}
          </div>
        ))}
        
        {/* Calendar Days */}
        {days.map(day => {
          const dayTasks = getTasksForDay(day);
          const isCurrentMonth = isSameMonth(day, currentDate);
          const isTodayDate = isToday(day);
          
          return (
            <div 
              key={day.toString()} 
              className={`calendar-day ${!isCurrentMonth ? 'other-month' : ''} ${isTodayDate ? 'today' : ''}`}
              onClick={() => handleDateClick(day)}
            >
              <div className="day-number">
                {format(day, 'd')}
              </div>
              
              <div className="day-tasks">
                {dayTasks.map(task => (
                  <TaskCard 
                    key={task.id}
                    task={task}
                    onComplete={() => handleTaskComplete(task.id)}
                    compact={true}
                  />
                ))}
                
                {dayTasks.length > 2 && (
                  <div className="more-tasks">
                    +{dayTasks.length - 2} mais
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Quick Add Modal */}
      {showQuickAdd && (
        <QuickAddModal 
          selectedDate={selectedDate}
          onSave={handleQuickAdd}
          onClose={() => setShowQuickAdd(false)}
        />
      )}
    </div>
  );
};

export default Calendar;