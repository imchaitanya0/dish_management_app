import React, { useState, useEffect } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import './App.css';

const BACKEND_URL = 'http://localhost:5000';

function App() {
  const [dishes, setDishes] = useState([]);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    fetchDishes();
    const newSocket = io(BACKEND_URL);
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (socket) {
      socket.on('dish_updated', (updatedDish) => {
        setDishes(prevDishes =>
          prevDishes.map(dish =>
            dish.dish_id === updatedDish.dish_id ? updatedDish : dish
          )
        );
      });
    }
  }, [socket]);

  const fetchDishes = async () => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/dishes`);
      setDishes(response.data);
    } catch (error) {
      console.error('Error fetching dishes:', error);
    }
  };

  const togglePublish = async (id) => {
    try {
      await axios.put(`${BACKEND_URL}/api/dishes/${id}/toggle-publish`);
    } catch (error) {
      console.error('Error toggling publish status:', error);
    }
  };

  return (
    <div className="App">
      <h1>Dish Dashboard</h1>
      <div className="dish-list">
        {dishes.map((dish) => (
          <div key={dish.dish_id} className="dish-item">
            <img src={dish.image_url} alt={dish.dish_name} />
            <h3>{dish.dish_name}</h3>
            <p>Status: {dish.is_published ? 'Published' : 'Unpublished'}</p>
            <button onClick={() => togglePublish(dish.dish_id)}>
              {dish.is_published ? 'Unpublish' : 'Publish'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;