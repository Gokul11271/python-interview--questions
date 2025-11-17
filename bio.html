import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../utils/auth";
import { UserCircleIcon, ShieldCheckIcon } from "@heroicons/react/24/outline";
import Beams from "../Components/Beams"; // <-- ADD THIS

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Admin");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    if (login(email, password, role)) {
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
        flex-1 flex items-center justify-center space-x-2 py-2 px-4 text-sm font-semibold rounded-lg transition duration-300 
        ${
          role === currentRole
            ? "bg-blue-600 text-white shadow-lg"
            : "bg-white/20 backdrop-blur-md text-white hover:bg-white/30"
        }
      `}
    >
      {icon}
      <span>{label}</span>
    </button>
  );

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* 🔥 BACKGROUND ANIMATION */}
      <div className="absolute inset-0 -z-10">
        <Beams
          beamWidth={2}
          beamHeight={15}
          beamNumber={12}
          lightColor="#ffffff"
          speed={2}
          noiseIntensity={1.75}
          scale={0.25}
          rotation={30}
        />
      </div>

      {/* LOGIN CONTAINER */}
      <div className="flex items-center justify-center min-h-screen px-4">
        {/* 🔥 GLASS + GRADIENT LOGIN CARD */}
        <div
          className="w-full max-w-md p-8 rounded-2xl shadow-2xl
                        bg-gradient-to-br from-white/10 via-white/5 to-white/10
                        backdrop-blur-xl border border-white/30 text-white space-y-10"
        >
          {/* Title */}
          <div className="text-center space-y-2">
            <h2 className="text-4xl font-extrabold drop-shadow">Sign In</h2>
            <p className="text-lg opacity-80">ERP System</p>
          </div>

          {/* Role Selection */}
          <div className="flex space-x-3 p-1 bg-white/10 backdrop-blur-lg border border-white/20 rounded-lg">
            <RolePill
              currentRole="Admin"
              icon={<ShieldCheckIcon className="w-5 h-5" />}
              label="Admin"
              onClick={() => setRole("Admin")}
            />
            <RolePill
              currentRole="User"
              icon={<UserCircleIcon className="w-5 h-5" />}
              label="Staff"
              onClick={() => setRole("User")}
            />
          </div>

          {error && (
            <p className="text-sm text-red-300 text-center bg-red-700/30 p-3 rounded-lg border border-red-400/40">
              {error}
            </p>
          )}

          {/* FORM */}
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email */}
            <div className="relative group">
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="peer w-full h-14 px-4 pt-5 bg-white/10 text-white placeholder-transparent
                           border-b-2 border-white/40 focus:border-blue-300 focus:outline-none backdrop-blur-lg"
                placeholder=" "
              />
              <label
                htmlFor="email"
                className="absolute left-3 top-3 text-white/70 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:top-4 peer-focus:top-2 peer-focus:text-sm"
              >
                Email Address
              </label>
            </div>

            {/* Password */}
            <div className="relative group">
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="peer w-full h-14 px-4 pt-5 bg-white/10 text-white placeholder-transparent
                           border-b-2 border-white/40 focus:border-blue-300 focus:outline-none backdrop-blur-lg"
                placeholder=" "
              />
              <label
                htmlFor="password"
                className="absolute left-3 top-3 text-white/70 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:top-4 peer-focus:top-2 peer-focus:text-sm"
              >
                Password
              </label>
            </div>

            {/* LOGIN BUTTON */}
            <button
              type="submit"
              className="w-full py-3 font-bold text-lg rounded-lg shadow-xl
                         bg-gradient-to-r from-blue-600 to-blue-400 hover:from-blue-700 hover:to-blue-500
                         transition-transform active:scale-95"
            >
              Sign In
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
