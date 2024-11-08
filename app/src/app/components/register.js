"use client";
import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { toast } from "react-toastify";

const Register = () => {
  const [loading, setLoading] = useState(false);

  // Formik setup
  const formik = useFormik({
    initialValues: {
      first_name: "",
      last_name: "",
      email: "",
      phone: "",
      password: "",
    },
    validationSchema: Yup.object({
      first_name: Yup.string().required("First name is required"),
      last_name: Yup.string().required("Last name is required"),
      email: Yup.string().email("Invalid email address").required("Email is required"),
      phone: Yup.string().required("Phone number is required"),
      password: Yup.string().min(6, "Password must be at least 6 characters").required("Password is required"),
    }),
    onSubmit: async (values) => {
      setLoading(true);
      try {
        const res = await fetch("/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        });

        if (!res.ok) {
          throw new Error("Registration failed");
        }

        const data = await res.json();
        toast.success(data.message || "Registration successful!");
      } catch (error) {
        toast.error(error.message || "An error occurred. Please try again.");
      } finally {
        setLoading(false);
      }
    },
  });

  return (
    <div
      className="h-screen w-screen flex items-center justify-center p-4"
      style={{
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundColor: "white",
      }}
    >
      <div className="max-w-4xl w-full p-8 shadow-lg rounded-lg flex">
        {/* Left Column with Catchy Phrase */}
        <div
          className="w-1/2 p-8 flex items-center justify-center"
          style={{
            backgroundColor: "#B8C4BB",
            color: "#333",
            fontFamily: "'Playfair Display', serif",
            fontSize: "2rem",
            fontWeight: "bold",
          }}
        >
          <div
            className="bg-transparent text-center"
            style={{
              fontFamily: "'Playfair Display', serif",
              fontSize: "2.5rem",
              fontWeight: "bold",
              color: "#333",
            }}
          >
            Welcome to the Team, Let's Start Your Journey!
          </div>
        </div>

        {/* Right Column with Form */}
        <div
          className="w-1/2 p-8"
          style={{
            backgroundColor: "#E8F7EE",
          }}
        >
          <h2 className="text-3xl font-bold text-center mb-6" style={{ color: "#000000" }}>
            Register
          </h2>
          <form onSubmit={formik.handleSubmit}>
            {/* First Name Field */}
            <div className="mb-6">
              <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                First Name
              </label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-[#63C132] focus:border-[#63C132] text-gray-700"
                onChange={formik.handleChange}
                value={formik.values.first_name}
              />
              {formik.errors.first_name && formik.touched.first_name && (
                <div className="text-red-600 text-sm mt-1">{formik.errors.first_name}</div>
              )}
            </div>

            <div className="mb-6">
              <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                Last Name
              </label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-[#63C132] focus:border-[#63C132] text-gray-700"
                onChange={formik.handleChange}
                value={formik.values.last_name}
              />
              {formik.errors.last_name && formik.touched.last_name && (
                <div className="text-red-600 text-sm mt-1">{formik.errors.last_name}</div>
              )}
            </div>

            <div className="mb-6">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-[#63C132] focus:border-[#63C132] text-gray-700"
                onChange={formik.handleChange}
                value={formik.values.email}
              />
              {formik.errors.email && formik.touched.email && (
                <div className="text-red-600 text-sm mt-1">{formik.errors.email}</div>
              )}
            </div>

            <div className="mb-6">
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <input
                type="text"
                id="phone"
                name="phone"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-[#63C132] focus:border-[#63C132] text-gray-700"
                onChange={formik.handleChange}
                value={formik.values.phone}
              />
              {formik.errors.phone && formik.touched.phone && (
                <div className="text-red-600 text-sm mt-1">{formik.errors.phone}</div>
              )}
            </div>

            <div className="mb-6">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-[#63C132] focus:border-[#63C132] text-gray-700"
                onChange={formik.handleChange}
                value={formik.values.password}
              />
              {formik.errors.password && formik.touched.password && (
                <div className="text-red-600 text-sm mt-1">{formik.errors.password}</div>
              )}
            </div>
            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-4 border border-transparent rounded-lg text-white ${
                loading ? "bg-gray-400" : "hover:opacity-90 focus:ring-4 focus:ring-green-400"
              }`}
              style={{
                background: loading
                  ? "bg-gray-400"
                  : "#B8C4BB",
              }}
            >
              {loading ? "Registering..." : "Register"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
