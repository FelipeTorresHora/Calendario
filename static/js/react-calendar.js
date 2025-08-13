// Simple React Calendar Component
document.addEventListener('DOMContentLoaded', function() {
  const calendarElement = document.getElementById('react-calendar');
  
  if (calendarElement && window.React && window.ReactDOM) {
    const tasksData = JSON.parse(calendarElement.dataset.tasks || '[]');
    const userId = calendarElement.dataset.userId;
    
    // Calendar Component
    function Calendar({ tasks, userId }) {
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
      
      const handleTaskComplete = async (taskId) => {
        try {
          const response = await fetch(`/tasks/${taskId}/complete/`, {
            method: 'POST',
            headers: {
              'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
              'Content-Type': 'application/json',
            },
          });
          
          if (response.ok) {
            // Reload page to update data
            window.location.reload();
          }
        } catch (error) {
          console.error('Error completing task:', error);
        }
      };
      
      const days = getDaysInMonth(currentDate);
      
      return React.createElement('div', { 
        className: 'react-calendar',
        style: {
          background: 'white',
          borderRadius: '12px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
          overflow: 'hidden',
        }
      },
        // Header
        React.createElement('div', { 
          className: 'calendar-header',
          style: {
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '20px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white'
          }
        },
          React.createElement('div', { 
            className: 'calendar-nav',
            style: { display: 'flex', alignItems: 'center', gap: '20px' }
          },
            React.createElement('button', { 
              onClick: goToPreviousMonth, 
              className: 'nav-btn',
              style: {
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: 'white',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                fontSize: '18px',
                cursor: 'pointer'
              }
            }, '←'),
            React.createElement('h2', { 
              className: 'current-month',
              style: { margin: 0, fontSize: '24px', fontWeight: '600' }
            }, `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`),
            React.createElement('button', { 
              onClick: goToNextMonth, 
              className: 'nav-btn',
              style: {
                background: 'rgba(255, 255, 255, 0.2)',
                border: 'none',
                color: 'white',
                width: '40px',
                height: '40px',
                borderRadius: '50%',
                fontSize: '18px',
                cursor: 'pointer'
              }
            }, '→')
          )
        ),
        
        // Calendar Grid
        React.createElement('div', { 
          className: 'calendar-grid',
          style: {
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: '1px',
            background: '#e5e7eb'
          }
        },
          // Weekday headers
          ...weekDays.map(day => 
            React.createElement('div', { 
              key: day, 
              className: 'weekday-header',
              style: {
                background: '#f9fafb',
                padding: '12px',
                textAlign: 'center',
                fontWeight: '600',
                color: '#6b7280',
                fontSize: '12px'
              }
            }, day)
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
              style: {
                background: isToday ? '#eff6ff' : 'white',
                minHeight: '100px',
                padding: '8px',
                cursor: day ? 'pointer' : 'default',
                border: isToday ? '2px solid #3b82f6' : 'none'
              },
              onClick: day ? () => setSelectedDate(day) : undefined
            },
              day && React.createElement('div', { 
                className: 'day-number',
                style: { 
                  fontWeight: '600', 
                  fontSize: '14px', 
                  marginBottom: '4px',
                  color: isToday ? '#3b82f6' : '#000'
                }
              }, day),
              day && React.createElement('div', { className: 'day-tasks' },
                ...dayTasks.slice(0, 2).map(task => 
                  React.createElement('div', { 
                    key: task.id, 
                    className: `task-indicator ${task.is_done ? 'completed' : ''}`,
                    style: {
                      background: task.is_done ? '#d1fae5' : '#fef3c7',
                      border: `1px solid ${task.is_done ? '#10b981' : '#f59e0b'}`,
                      borderRadius: '4px',
                      padding: '2px 6px',
                      fontSize: '10px',
                      marginBottom: '2px',
                      textDecoration: task.is_done ? 'line-through' : 'none',
                      cursor: 'pointer'
                    },
                    onClick: (e) => {
                      e.stopPropagation();
                      if (!task.is_done) {
                        handleTaskComplete(task.id);
                      }
                    }
                  }, task.description.substring(0, 15) + (task.description.length > 15 ? '...' : ''))
                ),
                dayTasks.length > 2 && 
                  React.createElement('div', { 
                    className: 'more-tasks',
                    style: {
                      background: '#e5e7eb',
                      color: '#6b7280',
                      fontSize: '10px',
                      padding: '2px 6px',
                      borderRadius: '8px',
                      textAlign: 'center',
                      marginTop: '2px'
                    }
                  }, `+${dayTasks.length - 2} mais`)
              )
            );
          })
        )
      );
    }
    
    // Render Calendar
    const root = ReactDOM.createRoot(calendarElement);
    root.render(React.createElement(Calendar, { tasks: tasksData, userId: userId }));
  } else {
    console.error('React Calendar: Missing React, ReactDOM or calendar element');
  }
});