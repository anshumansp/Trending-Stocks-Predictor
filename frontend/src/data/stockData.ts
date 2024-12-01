export const sectorData = {
  monthlyTopPerformers: [
    { sector: "IT", return: "2.6%" },
    { sector: "Bank", return: "0.7%" },
    { sector: "Pharma", return: "0.2%" }
  ],
  quarterlyTopPerformers: [
    { sector: "Auto", return: "N/A" },
    { sector: "Bank", return: "N/A" },
    { sector: "Financial Services", return: "N/A" }
  ],
  sectorDetails: [
    {
      name: "Bank",
      stocks: 5,
      monthReturn: "0.7%",
      quarterReturn: "N/A",
      topStocks: [
        { name: "HDFC Bank Limited", return: "3.5%" },
        { name: "State Bank of India", return: "2.0%" },
        { name: "Kotak Mahindra Bank Limited", return: "1.8%" }
      ]
    },
    {
      name: "IT",
      stocks: 5,
      monthReturn: "2.6%",
      quarterReturn: "N/A",
      topStocks: [
        { name: "Tata Consultancy Services Limited", return: "4.6%" },
        { name: "Infosys Limited", return: "3.1%" },
        { name: "Tech Mahindra Limited", return: "2.5%" }
      ]
    },
    {
      name: "Auto",
      stocks: 5,
      monthReturn: "-2.1%",
      quarterReturn: "N/A",
      topStocks: [
        { name: "Mahindra & Mahindra Limited", return: "9.5%" },
        { name: "Maruti Suzuki India Limited", return: "-1.6%" },
        { name: "Hero MotoCorp Limited", return: "-3.0%" }
      ]
    }
  ]
};

export const nifty50Data = {
  sectorPerformance: [
    { sector: "Technology", monthly: "2.6%", quarterly: "0.0%" },
    { sector: "Industrials", monthly: "0.4%", quarterly: "0.0%" },
    { sector: "Communication Services", monthly: "-0.4%", quarterly: "0.0%" },
    { sector: "Healthcare", monthly: "-0.4%", quarterly: "0.0%" },
    { sector: "Consumer Cyclical", monthly: "-2.4%", quarterly: "0.0%" }
  ],
  topStocks: [
    {
      name: "Mahindra & Mahindra Limited",
      sector: "Consumer Cyclical",
      monthReturn: "9.5%",
      price: "Rs. 2966.10",
      marketCap: "Rs. 3564.42B"
    },
    {
      name: "Larsen & Toubro Limited",
      sector: "Industrials",
      monthReturn: "9.3%",
      price: "Rs. 3724.80",
      marketCap: "Rs. 5118.23B"
    },
    {
      name: "Cipla Limited",
      sector: "Healthcare",
      monthReturn: "8.2%",
      price: "Rs. 1533.90",
      marketCap: "Rs. 1237.67B"
    },
    {
      name: "Bharat Electronics Limited",
      sector: "Industrials",
      monthReturn: "6.7%",
      price: "Rs. 308.00",
      marketCap: "Rs. 2248.85B"
    },
    {
      name: "Power Grid Corporation of India Limited",
      sector: "Utilities",
      monthReturn: "4.9%",
      price: "Rs. 329.40",
      marketCap: "Rs. 3063.15B"
    }
  ]
};
