import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../utils/auth";
import { UserCircleIcon, ShieldCheckIcon } from "@heroicons/react/24/outline";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Admin"); // New state for role
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // Pass the selected role to the login function
    if (login(email, password, role)) {
      // Redirect to the dashboard home route
      navigate("/home");
    } else {
      let hint;
      if (role === "Admin") {
        hint = "Invalid Admin credentials. Try: admin@kayaa.com / admin123";
      } else if (role === "User") {
        hint = "Invalid User credentials. Try: user@kayaa.com / user123";
      } else {
        hint = "Invalid credentials. Try: 123@gmail.com / 123";
      }
      setError(hint);
    }
  };

  const RolePill = ({ currentRole, icon, label, onClick }) => (
    <button
      type="button"
      onClick={onClick}
      className={`
        flex-1 flex items-center justify-center space-x-2 py-2 px-4 text-sm font-semibold rounded-lg transition duration-300 transform 
        ${
          role === currentRole
            ? "bg-blue-600 text-white shadow-md-2"
            : "bg-gray-100 text-gray-700 hover:bg-gray-200"
        }
        hover:scale-[1.01] active:scale-[0.99]
      `}
    >
      {icon}
      <span>{label}</span>
    </button>
  );

  return (
    // Clean, high-contrast background (Material Design Standard)
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      {/* Login Card Container */}
      <div className="w-full max-w-md space-y-10">
        {/* Header/Logo/Branding */}
        <div className="text-center mb-0 space-y-2">
          <div className="flex items-center justify-center text-blue-700 mb-2">
            <svg
              className="w-12 h-12"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="1.5"
                d="M12 8c1.657 0 3 .895 3 2s-1.343 2-3 2v5m0-10c-1.657 0-3 .895-3 2s1.343 2 3 2m-5 8h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2z"
              ></path>
            </svg>
          </div>
          <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            Sign In
          </h2>
          <p className="text-lg text-gray-500 font-medium">ERP System</p>
        </div>

        {/* Login Form Card - Pure White, Highest Elevation */}
        <form
          className="space-y-8 bg-white p-8 sm:p-10 rounded-xl shadow-xl-2 border border-gray-100"
          onSubmit={handleSubmit}
        >
          {/* Role Selection Segmented Control */}
          <div className="flex space-x-3 p-1 bg-gray-50 rounded-lg border border-gray-200 shadow-inner">
            <RolePill
              currentRole="Admin"
              icon={<ShieldCheckIcon className="w-5 h-5" />}
              label="Admin Access"
              onClick={() => setRole("Admin")}
            />
            <RolePill
              currentRole="User"
              icon={<UserCircleIcon className="w-5 h-5" />}
              label="Staff Login"
              onClick={() => setRole("User")}
            />
            {/* You can add 'Other' if needed, but keeping it to Admin/User for premium look */}
          </div>

          {/* Error Message */}
          {error && (
            <p className="text-sm font-semibold text-red-700 text-center bg-red-50 p-3 rounded-lg border border-red-200 transition duration-300">
              {error}
            </p>
          )}

          {/* Email Input - Floating Label with Sleek Animation */}
          <div className="relative group">
            <input
              id="email"
              name="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              // Sleek, minimal border, focus adds ring + primary color border
              className="peer w-full h-14 px-4 pt-5 pb-0 border-b-2 border-gray-300 bg-gray-50 text-base text-gray-900 placeholder-transparent focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition duration-300"
              placeholder=" "
            />
            <label
              htmlFor="email"
              // Label transition follows input focus
              className="absolute left-4 top-2.5 text-xs text-gray-500 transition-all duration-300 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-4 peer-focus:top-2.5 peer-focus:text-xs peer-focus:text-blue-600"
            >
              Email address
            </label>
          </div>

          {/* Password Input - Floating Label with Sleek Animation */}
          <div className="relative group pb-4">
            <input
              id="password"
              name="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="peer w-full h-14 px-4 pt-5 pb-0 border-b-2 border-gray-300 bg-gray-50 text-base text-gray-900 placeholder-transparent focus:outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100 transition duration-300"
              placeholder=" "
            />
            <label
              htmlFor="password"
              className="absolute left-4 top-2.5 text-xs text-gray-500 transition-all duration-300 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-4 peer-focus:top-2.5 peer-focus:text-xs peer-focus:text-blue-600"
            >
              Password
            </label>

            <div className="flex justify-end mt-2">
              <a
                href="#"
                className="text-sm font-medium text-blue-600 hover:text-blue-700 transition duration-300"
              >
                Forgot password?
              </a>
            </div>
          </div>

          {/* Sign In Button - Top-Tier Hover/Active Animation */}
          <div>
            <button
              type="submit"
              className="w-full flex justify-center py-3.5 px-4 rounded-lg shadow-lg-2 text-base font-semibold text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-transform-shadow transform duration-300 hover:scale-[1.005] active:scale-[0.99] active:shadow-md-2"
            >
              Access Dashboard
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
