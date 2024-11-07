"use client";

import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';

const RegisterSchema = Yup.object().shape({
  username: Yup.string().required('Required'),
  email: Yup.string().email('Invalid email').required('Required'),
  password: Yup.string().min(6, 'Too Short!').required('Required'),
});

export default function Register() {
  return (
    <div className="flex h-screen">
      {/* Left Side with Form */}
      <div className="w-1/2 bg-white flex flex-col justify-center p-8">
        <h2 className="text-4xl font-bold mb-4 text-gray-800">Join Us</h2>
        <p className="mb-8 text-gray-600">Unlock endless possibilities with us.</p>
        
        <Formik
          initialValues={{ username: '', email: '', password: '' }}
          validationSchema={RegisterSchema}
          onSubmit={(values) => {
            // Handle form submission
            console.log(values);
          }}
        >
          {({ errors, touched }) => (
            <Form className="space-y-6">
              <div>
                <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                  Username
                </label>
                <Field
                  id="username"
                  name="username"
                  placeholder="Enter your username"
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.username && touched.username ? (
                  <div className="text-red-500 text-sm">{errors.username}</div>
                ) : null}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email
                </label>
                <Field
                  id="email"
                  name="email"
                  type="email"
                  placeholder="Enter your email"
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.email && touched.email ? (
                  <div className="text-red-500 text-sm">{errors.email}</div>
                ) : null}
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <Field
                  id="password"
                  name="password"
                  type="password"
                  placeholder="Enter your password"
                  className="mt-1 block w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {errors.password && touched.password ? (
                  <div className="text-red-500 text-sm">{errors.password}</div>
                ) : null}
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500"
              >
                Register
              </button>
            </Form>
          )}
        </Formik>
      </div>

      {/* Right Side with Blurry Background Image */}
        <div
    className="w-1/2 relative"
    style={{
      backgroundImage: 'url(/green1.jpeg)', // Corrected here
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      filter: 'blur(5px)',
    }}
  >
    <div className="absolute inset-0 bg-black opacity-20"></div> {/* Overlay */}
  </div>

    </div>
  );
}
