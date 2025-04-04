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
            #full_url = f"{BASE_URL}{url_ender}"
            full_url = "https://thelowdown.com/reviews/endo/66957976-d9ed-4e0c-a9cc-2dc7e0a3419a"
            response = requests.get(full_url)  # Fetch HTML from URL
            soup = BeautifulSoup(response.text, "html.parser")  # Parse HTML
            elements = soup.select(
                "div.MuiGrid-root.MuiGrid-item.experienceCardstyle__ExperienceCardWrapper-sc-1xq63fy-0.kHtMxN.css-1wxaqej div.MuiGrid-root.MuiGrid-item.symptom.css-1wxaqej")  # Locate elements specifically within the targeted div
            
            # Dictionaries to hold symptoms and treatment data for a single review
            symptoms_data = {'link': full_url}
            treatment_data = {'link': full_url}

            is_treatment_section = False  # Track the current section state (symptoms vs treatments)

            for element in elements:  # Traverse through elements
                # Detect section change based on the title element
                if not is_treatment_section:
                    title_element = element.find_previous("p",
                                                          class_="MuiTypography-root MuiTypography-body1 symptoms-title css-k9a92g")
                    if title_element and "All treatments tried" in title_element.get_text():
                        is_treatment_section = True  # Switch to treatment section

                p_element = element.find("p", class_="MuiTypography-root MuiTypography-body2 css-1e2c98a")  # Find p
                div_element = element.find("div", class_=lambda
                    c: c and "experienceCardstyle__SymptomLabel" in c)  # Find div with variable class name
                if p_element:
                    p_text = p_element.text.strip()
                else:
                    alt_p_element = element.find("p", class_="MuiTypography-root MuiTypography-body1 css-k9a92g")
                    p_text = (
                        alt_p_element.find("b").text.strip()
                        if alt_p_element and alt_p_element.find("b")
                        else "No p-text found"
                    )

                div_text = div_element.text.strip() if div_element else "No description found"  # Get div text, provide default if absent

                print(p_text, div_text)

                # Combine the symptom description with its intensity level
                combined_text = f"{div_text}".strip()
                if not is_treatment_section:  # Add to symptoms before reaching treatment section
                    symptoms_data[p_text] = combined_text  # Map the symptom with its intensity
                    symptoms_headers_set.add(p_text)  # Collect unique symptom headers
                else:  # Add to treatments in the treatment section
                    # Look for additional comments if the treatment section is based on alternative p_text
                    treatment_comment = ""
                    if "No p-text found" not in p_text:
                        print("here")
                        comment_element = element.find("p", class_="MuiTypography-root MuiTypography-body2 css-1e2c98a")
                        treatment_comment = comment_element.text.strip() if comment_element and comment_element != p_element else ""
                        print(comment_element.text)

                    treatment_data[p_text] = {
                        "intensity": combined_text,
                        "comment": treatment_comment,
                    }  # Update treatment data with intensity and comments
                    treatments_headers_set.add(p_text)  # Collect unique treatment headers
                    print(treatment_comment)

            # Append this review's data to symptoms and treatments datasets
            all_symptoms_data.append(symptoms_data)
            all_treatments_data.append(treatment_data)
            # Extract review text
            review_text_element = soup.find("p", class_="MuiTypography-root MuiTypography-body1 css-k9a92g")
            review_text = review_text_element.get_text(strip=True) if review_text_element else "No review text found"
            print(full_url)
            print(all_treatments_data)

            # Add review text to a new dictionary
            review_data = {'link': full_url, 'review_text': review_text}
            all_reviews_data.append(review_data)
            break

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
    f"{header} (intensity)" for header in treatments_headers_set
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
                flattened_data[f"{key} (intensity)"] = value.get("intensity", "")
                flattened_data[f"{key} (comment)"] = value.get("comment", "")
        flattened_treatments_data.append(flattened_data)
    writer.writerows(flattened_treatments_data)  # Write all flattened treatment rows
