import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="flex items-center justify-center">
      <div
        className="
          h-10 w-10 
          rounded-full 
          border-4 border-t-4 
          border-gray-200 border-t-blue-500 
          animate-spin
        "
      ></div>
    </div>
  );
};

export default LoadingSpinner;