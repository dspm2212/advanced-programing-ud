// main.js
import React, { useState } from "react";
import ReactDOM from "react-dom";

function App() {
  const [eventType, setEventType] = useState("public");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const eventData = {
      name: formData.get("event-name"),
      description: formData.get("event-description"),
      type: formData.get("event-type"),
      password: formData.get("password"),
    };

    try {
      const response = await fetch("/api/events", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(eventData),
      });

      if (!response.ok) {
        throw new Error("Failed to create event");
      }

      alert("Event created successfully");
    } catch (error) {
      console.error(error);
      alert("An error occurred while creating the event");
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Create a Virtual Xperience</h1>
        <p>Choose if your event will be public or private.</p>
      </div>
      <div className="card">
        <div className="card-header">
          <h2>Event Details</h2>
        </div>
        <div className="card-content">
          <form id="event-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="event-name">Event Name</label>
              <input id="event-name" name="event-name" placeholder="Enter event name" required />
            </div>
            <div className="form-group">
              <label htmlFor="event-description">Event Description</label>
              <textarea id="event-description" name="event-description" placeholder="Enter event description" rows="3" required></textarea>
            </div>
            <div className="form-group">
              <label htmlFor="event-type">Event Type</label>
              <select id="event-type" name="event-type" value={eventType} onChange={(e) => setEventType(e.target.value)}>
                <option value="public">Public</option>
                <option value="private">Private</option>
              </select>
            </div>
            {eventType === "private" && (
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input id="password" name="password" type="password" placeholder="Enter password" required />
                <p className="text-sm text-gray-500">
                  This password will be required for guests to access the event.
                </p>
              </div>
            )}
            <div className="flex justify-end">
              <button type="submit" className="button">Create Event</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
