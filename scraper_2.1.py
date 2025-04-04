import requests
from bs4 import BeautifulSoup
import csv

# Define base URL for the reviews
BASE_URL = "https://thelowdown.com"

# Initialize lists to store data for CSV processing
all_symptoms_data = []  # Each entry represents a row of symptoms data for the CSV
all_treatments_data = []  # Each entry represents a row of treatment data for the CSV
all_reviews_data = []  # Each entry represents a row of review text data for the CSV
symptoms_headers_set = set()  # Maintain unique symptom headers
treatments_headers_set = set()  # Maintain unique treatment headers

# Read and process the reviews file
with open("reviews.txt", "r") as file:
    for line in file:
        url_ender = line.strip()  # Remove trailing whitespace
        if url_ender:  # Ensure line is not empty
            full_url = f"{BASE_URL}{url_ender}"
            response = requests.get(full_url)  # Fetch HTML from URL

            # Set up HTML Parser
            soup = BeautifulSoup(response.text, "html.parser")

            # Dictionaries to hold symptoms and treatment data for a single review
            symptoms_data = {'link': full_url}
            treatment_data = {'link': full_url}

            # Select the elements that have the
            elements = soup.select("div.MuiGrid-root.MuiGrid-item.experienceCardstyle__ExperienceCardWrapper-sc-1xq63fy-0.kHtMxN.css-1wxaqej div.MuiGrid-root.MuiGrid-item.symptom.css-1wxaqej")  # Locate elements specifically within the targeted div

            is_treatment_section = False  # Track the current section state (symptoms vs treatments)
            is_treatment_comment_section = False

            for element in elements:  # Traverse through elements
                # Detect section change based on the title element
                if not is_treatment_section:
                    title_element = element.find_previous("p",
                                                          class_="MuiTypography-root MuiTypography-body1 symptoms-title css-k9a92g")
                    if title_element and "All treatments tried" in title_element.get_text():
                        is_treatment_section = True  # Switch to treatment section
                        is_treatment_comment_section = False
                    elif title_element and "Treatments reviewed" in title_element.get_text():
                        is_treatment_comment_section = True # Switch to treatment comments section

                # Handle treatments with reviews
                if is_treatment_comment_section:
                    p_element = element.find("p", class_="MuiTypography-root MuiTypography-body1 css-k9a92g")
                    if p_element:
                        p_text = p_element.text.strip()
                    div_element = element.find("div", class_=lambda
                        c: c and "experienceCardstyle__SymptomLabel" in c)  # Find div with variable class name
                    t_review = element.find_next("p", class_="MuiTypography-root MuiTypography-body2 css-1e2c98a")

                else:
                    p_element = element.find("p", class_="MuiTypography-root MuiTypography-body2 css-1e2c98a")  # Find p
                    div_element = element.find("div", class_=lambda
                        c: c and "experienceCardstyle__SymptomLabel" in c)  # Find div with variable class name
                    if p_element:
                        p_text = p_element.text.strip()
                    div_text = div_element.text.strip() if div_element else "No description found"  # Get div text, provide default if absent


                # Combine the symptom description with its intensity level
                combined_text = f"{div_text}".strip()
                if not is_treatment_section and not is_treatment_comment_section:  # Add to symptoms before reaching treatment section
                    symptoms_data[p_text] = combined_text  # Map the symptom with its intensity
                    symptoms_headers_set.add(p_text)  # Collect unique symptom headers
                elif is_treatment_comment_section and not is_treatment_section:  # Add to treatments in the treatment section
                    # Look for additional comments if the treatment section is based on alternative p_text
                    if t_review:
                        treatment_comment = t_review.text.strip() if t_review and t_review != p_element else ""

                    treatment_data[p_text] = {
                        "effectivity": combined_text,
                        "comment": treatment_comment,
                    }  # Update treatment data with intensity and comments
                    treatments_headers_set.add(p_text)  # Collect unique treatment
                else:
                    if p_text not in treatment_data:
                        treatment_data[p_text] = {
                            "effectivity": combined_text,
                            "comment": "",
                        }  # Update treatment data with intensity and comments
                        treatments_headers_set.add(p_text)  # Collect unique treatment
                    ### TRY PRINTING THE SPECIFIC ELEMENT IN DICTIONARY

            # Append this review's data to symptoms and treatments datasets
            all_symptoms_data.append(symptoms_data)
            all_treatments_data.append(treatment_data)
            # Extract review text
            review_text_element = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-k9a92g")
            review_text = review_text_element.get_text(strip=True) if review_text_element else "No review text found"

            # Add review text to a new dictionary
            review_data = {'link': full_url, 'review_text': review_text}
            all_reviews_data.append(review_data)



# Write review text data to a CSV file
review_headers = ['link', 'review_text']  # Define headers for review text CSV
with open("reviews_output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=review_headers)
    writer.writeheader()  # Write the header row for reviews
    writer.writerows(all_reviews_data)  # Write all review text rows

# Write symptoms data to a CSV file
symptoms_headers = ['link'] + list(symptoms_headers_set)  # Add 'link' as the first column header for symptoms
with open("symptoms_output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=symptoms_headers)
    writer.writeheader()  # Write the header row for symptoms
    writer.writerows(all_symptoms_data)  # Write all symptoms rows

# Write treatments data to a CSV file
treatments_headers = ['link'] + [
    f"{header} (effectivity)" for header in treatments_headers_set
] + [f"{header} (comment)" for header in treatments_headers_set]  # Add headers for intensity and comments
with open("treatment_output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=treatments_headers)
    writer.writeheader()  # Write the header row for treatments
    # Flatten treatment data dictionaries to match headers
    flattened_treatments_data = []
    for data in all_treatments_data:
        flattened_data = {"link": data["link"]}
        for key, value in data.items():
            if key != "link":
                flattened_data[f"{key} (effectivity)"] = value.get("effectivity", "")
                flattened_data[f"{key} (comment)"] = value.get("comment", "")
        flattened_treatments_data.append(flattened_data)
    writer.writerows(flattened_treatments_data)  # Write all flattened treatment rows
