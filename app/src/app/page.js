import Register from './components/register';
import "react-toastify/dist/ReactToastify.css";
import { ToastContainer } from "react-toastify";  

export default function Page() {
  return (
    <div className="h-screen flex items-center justify-center">
      <Register />
      <ToastContainer />
    </div>
  );
}
