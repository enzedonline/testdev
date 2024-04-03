
// Define your custom function using ES6 arrow function
const extendModalWorkflow = (modalWorkflow) => {
    // Return a new function that wraps the original function
    return (...args) => {
        // Optionally, call the original function with the provided arguments
        modalWorkflow.apply(this, args);
  
        // Your custom functionality here
        console.log(args);
    };
  };
  
  // Extend window.ModalWorkflow function
  window.ModalWorkflow = extendModalWorkflow(window.ModalWorkflow);