// Dummy data for testing (replace with actual data from the backend)
var dummyData = [
    {
      name: "Student 1",
      roll: "23A8001",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 2",
      roll: "23A8002",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 3",
      roll: "23A8003",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 4",
      roll: "23A8004",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 5",
      roll: "23A8005",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 6",
      roll: "23A8006",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 7",
      roll: "23A8007",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 8",
      roll: "23A8008",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 9",
      roll: "23A8009",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    {
      name: "Student 10",
      roll: "23A8010",
      image: "https://cdn-icons-png.flaticon.com/512/666/666201.png",
    },
    // Add more dummy data as needed
  ];
  
  var currentVisibleIndex = dummyData.length; // Initialize currentVisibleIndex
  var labelsElement = document.getElementById("labels");
  var noResultsMessageElement = document.getElementById("noResultsMessage");
  
  // Function to populate the leaderboard with data
  function populateLeaderboard(data) {
    if (data.length > 0) {
      // Show labels and hide "No results found" message
      labelsElement.style.display = "flex";
      noResultsMessageElement.style.display = "none";
    } else {
      // Hide labels and show "No results found" message
      labelsElement.style.display = "none";
      noResultsMessageElement.style.display = "block";
    }
    var leaderboard = document.getElementById("leaderboard");
  
    if (!leaderboard) {
      console.error("Unable to find the leaderboard element");
      return;
    }
  
    // Clear current entries
    leaderboard.innerHTML = "";
  
    // Show "Show more" button if there are more entries
    // var showMoreBtn = document.getElementById("showMoreBtn");
    // if (showMoreBtn) {
    //   showMoreBtn.style.display =
    //     data.length > currentVisibleIndex ? "block" : "none";
    // }
  
    // Function to show more entries
    // function showMoreEntries() {
    //   var entries = document.querySelectorAll(".entry");
    //   for (
    //     var i = currentVisibleIndex;
    //     i < currentVisibleIndex + 5 && i < entries.length;
    //     i++
    //   ) {
    //     entries[i].style.display = "flex";
    //   }
  
    //   currentVisibleIndex += 5;
  
    //   // Hide "Show more" button if no more entries
    //   if (currentVisibleIndex >= entries.length && showMoreBtn) {
    //     showMoreBtn.style.display = "none";
    //   }
    // }
  
    data.slice(0, currentVisibleIndex).forEach((entry, index) => {
      var entryElement = document.createElement("div");
      entryElement.classList.add(
        "mb-4",
        "p-2",
        "hover:bg-gray-200",
        "hover:shadow-md",
        "rounded-full",
        "entry",
        "flex",
        "items-center",
        "justify-between"
      );
  
      // Create inner div for left content
      var leftDiv = document.createElement("div");
      leftDiv.classList.add("flex", "flex-row", "items-center");
  
      // Create image element
      var imgElement = document.createElement("img");
      imgElement.src = entry.image;
      imgElement.alt = entry.name;
      imgElement.classList.add(
        "mr-2",
        "rounded-full",
        "w-10",
        "h-10",
        "p-2",
        "border-2",
        "border-blue-400"
      );
  
      // Create div for text content
      var textDiv = document.createElement("div");
      textDiv.textContent = entry.name;
  
      // Append image and text content to left div
      leftDiv.appendChild(imgElement);
      leftDiv.appendChild(textDiv);
  
      // Create div for right content
      var rightDiv = document.createElement("div");
      rightDiv.textContent = `${entry.roll}`;
      rightDiv.classList.add("mr-4");
  
      // Append left and right divs to entry element
      entryElement.appendChild(leftDiv);
      entryElement.appendChild(rightDiv);
  
      entryElement.style.display = "flex";
      leaderboard.appendChild(entryElement);
    });
  
  //   // Add event listener for the "Show more" button
  //   if (showMoreBtn) {
  //     showMoreBtn.addEventListener("click", showMoreEntries);
  //   }
  }
  
  document.addEventListener("DOMContentLoaded", function () {
    if (dummyData.length > 0) {
      // Initial population with dummy data
      populateLeaderboard(dummyData);
  
      // Add event listener for the dropdown menu
    //   var sortSelect = document.getElementById("sortSelect");
    //   if (sortSelect) {
    //     sortSelect.addEventListener("change", function (event) {
    //       event.preventDefault();
    //       // Reset currentVisibleIndex when changing sorting direction
    //       currentVisibleIndex = 5;
  
    //       // Repopulate the leaderboard with the updated sorting direction
    //       populateLeaderboard(dummyData);
    //     });
    //   }
    // } else {
    //   document.getElementById("labels").style.display = "none";
    //   document.getElementById("noResultsMessage").style.display = "block";
    }
  });
  