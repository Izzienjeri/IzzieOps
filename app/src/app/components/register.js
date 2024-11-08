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
    <div className="flex flex-col lg:flex-row items-center justify-center min-h-screen bg-gray-100 p-8">
      {/* Marketing Side */}
      <div className="lg:w-1/2 w-full text-center lg:text-left lg:pr-10 mb-10 lg:mb-0">
        <h1 className="text-3xl font-bold text-[#358600] mb-6">
          Welcome to Our Community!
        </h1>
        <p className="text-lg text-gray-700 mb-4">
          Join us and start your journey today. Enjoy exclusive benefits, personalized content, and more.
        </p>
        <p className="text-lg text-gray-700">
          Become a part of something amazing. Sign up now!
        </p>
      </div>

      {/* Form Side */}
      <div className="lg:w-1/2 w-full max-w-lg p-8 bg-white shadow-lg rounded-lg">
        <h2 className="text-2xl font-bold text-[#358600] mb-6">Register</h2>
        <form onSubmit={formik.handleSubmit}>
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
            className={`w-full py-3 text-lg font-semibold rounded-md shadow-sm text-white ${loading ? "bg-gray-400" : "bg-[#358600] hover:bg-[#63C132]"} focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#63C132]`}
          >
            {loading ? "Registering..." : "Register"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
