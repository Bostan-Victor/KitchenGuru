import React, { useState } from 'react';
import './App.css';

function App() {
  const [isShown, setIsShown] = useState(false);

  return (
    <div className="App">
      <button
        onMouseEnter={() => setIsShown(true)}
        onMouseLeave={() => setIsShown(false)}>
        Hover over me!
      </button>
      {isShown && (
        <div>
          
        </div>
      )}
    </div>
  );
}

export default App;