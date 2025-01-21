import streamlit as st
import pandas as pd

# Dummy database for services with additional details, pricing, and coordinates for map display
data = {
    "Tailors": [
        {"Name": "Elegant Threads", "Specialty": "Custom suits", "Location": "Downtown", "Price Range": "$100 - $500", "Website": "https://www.elegantthreads.com", "Latitude": 59.9139, "Longitude": 10.7522},
        {"Name": "Stitch Perfect", "Specialty": "Alterations", "Location": "Uptown", "Price Range": "$50 - $200", "Website": "https://www.stitchperfect.com", "Latitude": 59.9239, "Longitude": 10.7622},
        {"Name": "Fashion Forward", "Specialty": "Bridal wear", "Location": "Midtown", "Price Range": "$300 - $1500", "Website": "https://www.fashionforward.com", "Latitude": 59.9039, "Longitude": 10.7422},
    ],
    "Medical": [
        {"Name": "Healthy Life Clinic", "Specialty": "General Practitioner", "Location": "East Side", "Price Range": "$50 - $100", "Website": "https://www.healthylifeclinic.com", "Latitude": 59.9130, "Longitude": 10.7800},
        {"Name": "Smile Dental", "Specialty": "Dentistry", "Location": "West End", "Price Range": "$100 - $300", "Website": "https://www.smiledental.com", "Latitude": 59.9111, "Longitude": 10.7322},
        {"Name": "Vision Center", "Specialty": "Optometry", "Location": "North Plaza", "Price Range": "$50 - $150", "Website": "https://www.visioncenter.com", "Latitude": 59.9200, "Longitude": 10.7500},
    ],
    "Tutors": [
        {"Name": "LearnSmart Tutors", "Specialty": "Math & Science", "Location": "City Center", "Price Range": "$20 - $50/hr", "Website": "https://www.learnsmarttutors.com", "Latitude": 59.9145, "Longitude": 10.7550},
        {"Name": "Language Pro", "Specialty": "French & Spanish", "Location": "Suburbia", "Price Range": "$25 - $60/hr", "Website": "https://www.languagepro.com", "Latitude": 59.9300, "Longitude": 10.7700},
        {"Name": "Tech Tutors", "Specialty": "Coding & Programming", "Location": "Tech District", "Price Range": "$30 - $70/hr", "Website": "https://www.techtutors.com", "Latitude": 59.9000, "Longitude": 10.7400},
    ],
    "Mechanics": [
        {"Name": "AutoFix Garage", "Specialty": "Engine repair", "Location": "Industrial Zone", "Price Range": "$100 - $1000", "Website": "https://www.autofixgarage.com", "Latitude": 59.8950, "Longitude": 10.7150},
        {"Name": "Quick Wheels", "Specialty": "Tire replacement", "Location": "Central Hub", "Price Range": "$50 - $200", "Website": "https://www.quickwheels.com", "Latitude": 59.9050, "Longitude": 10.7350},
        {"Name": "DriveSafe", "Specialty": "Brake services", "Location": "Highway Avenue", "Price Range": "$80 - $500", "Website": "https://www.drivesafe.com", "Latitude": 59.8900, "Longitude": 10.7100},
    ],
    "Event Planners": [
        {"Name": "Dream Weddings", "Specialty": "Wedding Planning", "Location": "Seaside", "Price Range": "$1000 - $5000", "Website": "https://www.dreamweddings.com", "Latitude": 59.8700, "Longitude": 10.6900},
        {"Name": "Corporate Pro", "Specialty": "Corporate Events", "Location": "Business Park", "Price Range": "$2000 - $10000", "Website": "https://www.corporatepro.com", "Latitude": 59.8600, "Longitude": 10.6800},
        {"Name": "Party Perfect", "Specialty": "Birthday Parties", "Location": "Entertainment District", "Price Range": "$500 - $2000", "Website": "https://www.partyperfect.com", "Latitude": 59.8800, "Longitude": 10.7000},
    ],
}

# Streamlit app setup
st.title("Service Marketplace")

# Create the page selector
page = st.selectbox("Navigate", ["Home", "Contact Form"])

# Home Page: Display the services
if page == "Home":
    # Tabs for services
    selected_tab = st.tabs(["Tailors", "Medical", "Tutors", "Mechanics", "Event Planners"])

    # Display data based on the selected tab
    for i, service_category in enumerate(data.keys()):
        with selected_tab[i]:
            st.header(f"Explore {service_category}")

            # Filters for narrowing the offers
            specialties = list(set(entry["Specialty"] for entry in data[service_category]))
            locations = list(set(entry["Location"] for entry in data[service_category]))

            selected_specialty = st.selectbox("Select a Specialty:", ["All"] + specialties, key=f"specialty-{service_category}")
            selected_location = st.selectbox("Select a Location:", ["All"] + locations, key=f"location-{service_category}")

            # Filter data based on user selection
            filtered_data = [
                entry for entry in data[service_category]
                if (selected_specialty == "All" or entry["Specialty"] == selected_specialty)
                and (selected_location == "All" or entry["Location"] == selected_location)
            ]

            # Display filtered results with details
            for entry in filtered_data:
                with st.expander(f"Details for {entry['Name']}"):
                    st.write(f"**Specialty:** {entry['Specialty']}")
                    st.write(f"**Location:** {entry['Location']}")
                    st.write(f"**Price Range:** {entry['Price Range']}")
                    st.write(f"**Website:** [Visit Website]({entry['Website']})")
                    contact_button = st.button(f"Contact {entry['Name']}", key=f"contact-{entry['Name']}")
                    if contact_button:
                        st.session_state["selected_provider"] = entry
                        # Navigate to the contact form page
                        st.experimental_set_query_params(page="Contact Form")
                        st.rerun()  # Trigger rerun to show the contact form

            # Display map for filtered locations
            if filtered_data:
                st.subheader("Service Locations")
                map_data = pd.DataFrame(
                    {
                        "lat": [entry["Latitude"] for entry in filtered_data],
                        "lon": [entry["Longitude"] for entry in filtered_data],
                        "name": [entry["Name"] for entry in filtered_data],
                    }
                )
                st.map(map_data)
            else:
                st.write("No services match your filters.")

elif page == "Contact Form":
    st.header("Contact Service Provider")

    if "selected_provider" in st.session_state:
        provider = st.session_state["selected_provider"]
        st.write(f"You are contacting **{provider['Name']}**")
        st.write(f"**Specialty:** {provider['Specialty']}")
        st.write(f"**Location:** {provider['Location']}")
        st.write(f"**Price Range:** {provider['Price Range']}")

        with st.form("contact_form"):
            user_name = st.text_input("Your Name")
            user_email = st.text_input("Your Email")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Send Message")

            if submitted:
                st.success("Your message has been sent!")
    else:
        st.write("No service provider selected. Please go back to the Home page and select a provider to contact.")
