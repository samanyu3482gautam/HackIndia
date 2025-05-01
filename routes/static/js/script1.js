// document.addEventListener('DOMContentLoaded', () => {
//   const flightForm = document.getElementById('flight-form');
//   const flightResultsContainer = document.getElementById('flight-results');
//   const departureInput = document.getElementById('departure');
//   const destinationInput = document.getElementById('destination');
//   const suggestionsBox = document.getElementById('suggestions');

//   // Example airports list (moved here for scope)
//   const airports = [
//     "Dubai (DXB) - Dubai Intl",
//     "London Heathrow (LHR) - Heathrow Airport",
//     "New York JFK (JFK) - John F. Kennedy Intl",
//     "Singapore Changi (SIN) - Changi Airport",
//     "Tokyo Narita (NRT) - Narita Intl",
//     "Albuquerque (ABQ) - Albuquerque International Sunport",
//     "Nantucket (ACK) - Nantucket Memorial Airport",
//     "Albany (ALB) - Albany International Airport",
//     "Atlanta (ATL) - Hartsfield-Jackson Atlanta International Airport",
//     "Austin (AUS) - Austin-Bergstrom International Airport",
//     "Asheville (AVL) - Asheville Regional Airport",
//     "Hartford (BDL) - Bradley International Airport",
//     "Bangor (BGR) - Bangor International Airport",
//     "Birmingham (BHM) - Birmingham-Shuttlesworth International Airport",
//     "Nashville (BNA) - Nashville International Airport",
//     "Boston (BOS) - Logan International Airport",
//     "Aguadilla (BQN) - Rafael Hernández Airport",
//     "Burlington (BTV) - Burlington International Airport",
//     "Buffalo (BUF) - Buffalo Niagara International Airport",
//     "Burbank (BUR) - Hollywood Burbank Airport",
//     "Baltimore (BWI) - Baltimore/Washington International Thurgood Marshall Airport",
//     "Bozeman (BZN) - Bozeman Yellowstone International Airport",
//     "Columbia (CAE) - Columbia Metropolitan Airport",
//     "Akron (CAK) - Akron-Canton Airport",
//     "Charleston (CHS) - Charleston International Airport",
//     "Cleveland (CLE) - Cleveland Hopkins International Airport",
//     "Charlotte (CLT) - Charlotte Douglas International Airport",
//     "Columbus (CMH) - John Glenn Columbus International Airport",
//     "Charleston (CRW) - Yeager Airport",
//     "Cincinnati (CVG) - Cincinnati/Northern Kentucky International Airport",
//     "Dayton (DAY) - Dayton International Airport",
//     "Washington D.C. (DCA) - Ronald Reagan Washington National Airport",
//     "Denver (DEN) - Denver International Airport",
//     "Dallas/Fort Worth (DFW) - Dallas/Fort Worth International Airport",
//     "Des Moines (DSM) - Des Moines International Airport",
//     "Detroit (DTW) - Detroit Metropolitan Wayne County Airport",
//     "Vail (EGE) - Eagle County Regional Airport",
//     "Key West (EYW) - Key West International Airport",
//     "Fort Lauderdale (FLL) - Fort Lauderdale-Hollywood International Airport",
//     "Grand Rapids (GRR) - Gerald R. Ford International Airport",
//     "Greensboro (GSO) - Piedmont Triad International Airport",
//     "Greenville (GSP) - Greenville-Spartanburg International Airport",
//     "Steamboat Springs (HDN) - Yampa Valley Airport",
//     "Honolulu (HNL) - Daniel K. Inouye International Airport",
//     "Houston (HOU) - William P. Hobby Airport",
//     "Washington D.C. (IAD) - Washington Dulles International Airport",
//     "Houston (IAH) - George Bush Intercontinental Airport",
//     "Wilmington (ILM) - Wilmington International Airport",
//     "Indianapolis (IND) - Indianapolis International Airport",
//     "Jackson (JAC) - Jackson Hole Airport",
//     "Jacksonville (JAX) - Jacksonville International Airport",
//     "Las Vegas (LAS) - Harry Reid International Airport",
//     "Los Angeles (LAX) - Los Angeles International Airport",
//     "Long Beach (LGB) - Long Beach Airport",
//     "Kansas City (MCI) - Kansas City International Airport",
//     "Orlando (MCO) - Orlando International Airport",
//     "Chicago (MDW) - Chicago Midway International Airport",
//     "Memphis (MEM) - Memphis International Airport",
//     "Manchester (MHT) - Manchester-Boston Regional Airport",
//     "Miami (MIA) - Miami International Airport",
//     "Milwaukee (MKE) - General Mitchell International Airport",
//     "Madison (MSN) - Dane County Regional Airport",
//     "Minneapolis (MSP) - Minneapolis-Saint Paul International Airport",
//     "New Orleans (MSY) - Louis Armstrong New Orleans International Airport",
//     "Montrose (MTJ) - Montrose Regional Airport",
//     "Martha's Vineyard (MVY) - Martha's Vineyard Airport",
//     "Myrtle Beach (MYR) - Myrtle Beach International Airport",
//     "Oakland (OAK) - Oakland International Airport",
//     "Oklahoma City (OKC) - Will Rogers World Airport",
//     "Omaha (OMA) - Eppley Airfield",
//     "Chicago (ORD) - O'Hare International Airport",
//     "Norfolk (ORF) - Norfolk International Airport",
//     "West Palm Beach (PBI) - Palm Beach International Airport",
//     "Portland (PDX) - Portland International Airport",
//     "Philadelphia (PHL) - Philadelphia International Airport",
//     "Phoenix (PHX) - Phoenix Sky Harbor International Airport",
//     "Pittsburgh (PIT) - Pittsburgh International Airport",
//     "Ponce (PSE) - Mercedita Airport",
//     "Palm Springs (PSP) - Palm Springs International Airport",
//     "Providence (PVD) - T.F. Green Airport",
//     "Portland (PWM) - Portland International Jetport",
//     "Raleigh (RDU) - Raleigh-Durham International Airport",
//     "Richmond (RIC) - Richmond International Airport",
//     "Rochester (ROC) - Greater Rochester International Airport",
//     "Fort Myers (RSW) - Southwest Florida International Airport",
//     "San Diego (SAN) - San Diego International Airport",
//     "San Antonio (SAT) - San Antonio International Airport",
//     "Savannah (SAV) - Savannah/Hilton Head International Airport",
//     "South Bend (SBN) - South Bend International Airport",
//     "Louisville (SDF) - Louisville Muhammad Ali International Airport",
//     "Seattle (SEA) - Seattle-Tacoma International Airport",
//     "San Francisco (SFO) - San Francisco International Airport",
//     "San Jose (SJC) - Norman Y. Mineta San Jose International Airport",
//     "San Juan (SJU) - Luis Muñoz Marín International Airport",
//     "Salt Lake City (SLC) - Salt Lake City International Airport",
//     "Sacramento (SMF) - Sacramento International Airport",
//     "Santa Ana (SNA) - John Wayne Airport",
//     "Sarasota (SRQ) - Sarasota–Bradenton International Airport",
//     "St. Louis (STL) - St. Louis Lambert International Airport",
//     "St. Thomas (STT) - Cyril E. King Airport",
//     "Syracuse (SYR) - Syracuse Hancock International Airport",
//     "Tampa (TPA) - Tampa International Airport",
//     "Tulsa (TUL) - Tulsa International Airport",
//     "Knoxville (TYS) - McGhee Tyson Airport",
//     "Fayetteville (XNA) - Northwest Arkansas National Airport",
//     "Newark (EWR) - Newark Liberty International Airport",
//     "New York (JFK) - John F. Kennedy International Airport",
//     "New York (LGA) - LaGuardia Airport"
//   ];

//   // Function to handle airport suggestions for a given input field
//   function setupAirportSuggestions(inputElement, suggestionsElement) {
//     inputElement.addEventListener("input", () => {
//       const input = inputElement.value.toLowerCase();
//       suggestionsElement.innerHTML = ""; // Clear previous suggestions

//       if (input === "") {
//         suggestionsElement.classList.add("hidden");
//         return;
//       }

//       const matches = airports.filter(airport => airport.toLowerCase().includes(input));

//       if (matches.length === 0) {
//         suggestionsElement.classList.add("hidden");
//         return;
//       }

//       matches.forEach(match => {
//         const li = document.createElement("li");
//         li.textContent = match;
//         li.addEventListener("click", () => {
//           inputElement.value = match;
//           suggestionsElement.classList.add("hidden");
//         });
//         suggestionsElement.appendChild(li);
//       });

//       suggestionsElement.classList.remove("hidden");
//     });

//     document.addEventListener("click", (event) => {
//       if (!inputElement.contains(event.target) && !suggestionsElement.contains(event.target)) {
//         suggestionsElement.classList.add("hidden");
//       }
//     });
//   }

//   // Setup suggestions for both departure and destination
//   const departureSuggestionsBox = document.createElement('ul');
//   departureSuggestionsBox.id = 'departure-suggestions';
//   departureSuggestionsBox.classList.add('suggestions', 'hidden');
//   departureInput.parentNode.appendChild(departureSuggestionsBox);
//   setupAirportSuggestions(departureInput, departureSuggestionsBox);

//   const destinationSuggestionsBox = document.createElement('ul');
//   destinationSuggestionsBox.id = 'destination-suggestions';
//   destinationSuggestionsBox.classList.add('suggestions', 'hidden');
//   destinationInput.parentNode.appendChild(destinationSuggestionsBox);
//   setupAirportSuggestions(destinationInput, destinationSuggestionsBox);


//   // Sample flight data (replace with actual API calls later)
//   const sampleFlights = [
//     {
//       airline: 'Indigo',
//       flightNumber: '6E 2001',
//       departure: 'San Diego (SAN) - San Diego International Airport',
//       destination: 'St. Thomas (STT) - Cyril E. King Airport',
//       departureTime: '10:00',
//       arrivalTime: '12:00',
//       price: 4500,
//     },
//     {
//       airline: 'SpiceJet',
//       flightNumber: 'SG 105',
//       departure: 'Delhi (DEL) - Indira Gandhi Intl',
//       destination: 'Mumbai (BOM) - Chhatrapati Shivaji Intl',
//       departureTime: '14:00',
//       arrivalTime: '16:15',
//       price: 4200,
//     },
//     {
//       airline: 'Air India',
//       flightNumber: 'AI 403',
//       departure: 'Chandigarh (IXC) - Shaheed Bhagat Singh Intl',
//       destination: 'Delhi (DEL) - Indira Gandhi Intl',
//       departureTime: '08:00',
//       arrivalTime: '08:50',
//       price: 2800,
//     },
//     {
//       airline: 'Emirates',
//       flightNumber: 'EK 501',
//       departure: 'Dubai (DXB) - Dubai Intl',
//       destination: 'London Heathrow (LHR) - Heathrow Airport',
//       departureTime: '15:30',
//       arrivalTime: '20:00',
//       price: 15000,
//     },
//     // Add more flight data here
//   ];

    flightForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const departure = document.getElementById('departure').value.trim().toUpperCase();
    const destination = document.getElementById('destination').value.trim().toUpperCase();
    const priority = document.getElementById('priority').value;

    flightResultsContainer.innerHTML = '<p>Loading...</p>';

    fetch(`/find_route/?start=${departure}&end=${destination}`)
      .then(response => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then(data => {
        console.log("Flight data from backend:", data);
        flightResultsContainer.innerHTML = "";

        const flights = data[priority === 'cost' ? 'minimum_cost' : 'earliest_arrival'].path_details;

        if (flights.length === 0) {
          flightResultsContainer.innerHTML = '<p>No flights found for your selection.</p>';
          return;
        }

        flights.forEach(flight => {
          const flightDiv = document.createElement('div');
          flightDiv.classList.add('flight-result-item');

          flightDiv.innerHTML = `
            <h3>${flight.airline_name} - ${flight.flight_number}</h3>
            <p>From: ${flight.origin} at ${flight.hour}:${String(flight.minute).padStart(2, '0')}</p>
            <p>To: ${flight.destination} at ${String(flight.arr_time).padStart(4, '0')}</p>
            <p>Cost: ₹${flight.flight_cost}</p>
            <p>Distance: ${flight.distance} km</p>
          `;

          flightResultsContainer.appendChild(flightDiv);
        });
      })
      .catch(error => {
        console.error("Error fetching flight data:", error);
        flightResultsContainer.innerHTML = '<p>Error loading flight data.</p>';
      });
  });
