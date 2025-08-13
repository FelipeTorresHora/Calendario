// Main entry point for React components
// Note: Using global React and ReactDOM from CDN

// Utils
const getCsrfToken = () => {
  return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
         document.querySelector('meta[name=csrf-token]')?.getAttribute('content') ||
         '';
};

const showToast = (message, type = 'info') => {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#3b82f6'};
    color: white;
    padding: 12px 20px;
    border-radius: 6px;
    z-index: 1000;
    transition: all 0.3s ease;
  `;
  
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
};

// Simple Calendar Component without external dependencies
const Calendar = ({ tasks, userId }) => {
  const [currentDate, setCurrentDate] = React.useState(new Date());
  const [selectedDate, setSelectedDate] = React.useState(null);
  
  const monthNames = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ];
  
  const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  
  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startDay = firstDay.getDay();
    
    const days = [];
    
    // Add empty cells for days before month starts
    for (let i = 0; i < startDay; i++) {
      days.push(null);
    }
    
    // Add days of month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(day);
    }
    
    return days;
  };
  
  const getTasksForDay = (day) => {
    if (!day || !tasks) return [];
    const dateStr = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return tasks.filter(task => task.date === dateStr);
  };
  
  const goToPreviousMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };
  
  const goToNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };
  
  const days = getDaysInMonth(currentDate);
  
  return React.createElement('div', { className: 'react-calendar' },
    // Header
    React.createElement('div', { className: 'calendar-header' },
      React.createElement('div', { className: 'calendar-nav' },
        React.createElement('button', { onClick: goToPreviousMonth, className: 'nav-btn' }, '←'),
        React.createElement('h2', { className: 'current-month' }, 
          `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`
        ),
        React.createElement('button', { onClick: goToNextMonth, className: 'nav-btn' }, '→')
      )
    ),
    
    // Calendar Grid
    React.createElement('div', { className: 'calendar-grid' },
      // Weekday headers
      ...weekDays.map(day => 
        React.createElement('div', { key: day, className: 'weekday-header' }, day)
      ),
      
      // Calendar days
      ...days.map((day, index) => {
        const dayTasks = getTasksForDay(day);
        const isToday = day && 
          currentDate.getFullYear() === new Date().getFullYear() &&
          currentDate.getMonth() === new Date().getMonth() &&
          day === new Date().getDate();
        
        return React.createElement('div', {
          key: index,
          className: `calendar-day ${!day ? 'empty' : ''} ${isToday ? 'today' : ''}`,
          onClick: day ? () => setSelectedDate(day) : undefined
        },
          day && React.createElement('div', { className: 'day-number' }, day),
          day && React.createElement('div', { className: 'day-tasks' },
            ...dayTasks.slice(0, 2).map(task => 
              React.createElement('div', { 
                key: task.id, 
                className: `task-indicator ${task.is_done ? 'completed' : ''}` 
              }, task.description.substring(0, 20))
            ),
            dayTasks.length > 2 && 
              React.createElement('div', { className: 'more-tasks' }, `+${dayTasks.length - 2} mais`)
          )
        );
      })
    )
  );
};

// Initialize components when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  // Calendar component
  const calendarElement = document.getElementById('react-calendar');
  if (calendarElement) {
    const root = createRoot(calendarElement);
    const tasksData = JSON.parse(calendarElement.dataset.tasks || '[]');
    const userId = calendarElement.dataset.userId;
    
    root.render(
      <Calendar 
        tasks={tasksData}
        userId={userId}
        csrfToken={getCsrfToken()}
      />
    );
  }

  // Task List component
  const taskListElement = document.getElementById('react-task-list');
  if (taskListElement) {
    const root = createRoot(taskListElement);
    const tasks = JSON.parse(taskListElement.dataset.tasks || '[]');
    
    root.render(
      <TaskList 
        tasks={tasks}
        csrfToken={getCsrfToken()}
      />
    );
  }

  // Metrics Chart component
  const metricsElement = document.getElementById('react-metrics');
  if (metricsElement) {
    const root = createRoot(metricsElement);
    const metricsData = JSON.parse(metricsElement.dataset.metrics || '{}');
    
    root.render(
      <MetricsChart 
        data={metricsData}
      />
    );
  }
});