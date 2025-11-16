import { createRoot } from "react-dom/client";

const App = () => {
  return <button onClick={() => alert("React works!")}>Click me</button>;
};

const container = document.getElementById("root")!;
createRoot(container).render(<App />);
