import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';


/**
 * Interface of the props passed into PriceHistory
 */ 
interface PriceHistoryProps {
  params: {
    priceHistory: {
      startDate: string;
      endDate: string;
      price: number;
    }[];
  }
}

/**
 * Renders an interactive line chart showing the price history of a product over time.
 */
export default function PriceHistory({ params }: PriceHistoryProps) {
  
  // Chart data array to hold date points and prices
  const chartData: any[] = [];

  // Label that pops up on price history hover
  const HoverLabel = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const price = payload[0].value;
      return (
        <div className="p-2 bg-gray-800 text-white rounded-md shadow-lg">
          <p className="font-bold">{`Price: $${price.toFixed(2)}`}</p>
          <p className="text-sm">{`Date: ${new Date(label).toLocaleDateString('en-AU')}`}</p>
        </div>
      );
    }
  };
  
  // Data logic to create chartData array
  params.priceHistory.forEach(entry => {

    const currentDateVar = new Date(entry.startDate);
    const endDateVar = new Date(entry.endDate)

    while (currentDateVar <= endDateVar) {
      chartData.push({
        date: currentDateVar.getTime(),
        price: entry.price,
      });
      currentDateVar.setDate(currentDateVar.getDate() + 1);
    }
  });
  chartData.sort((a, b) => a.date - b.date);

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-4xl">
      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <XAxis
              dataKey="date"
              type="number"
              domain={['auto', 'auto']}
              scale="time"
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-AU')}
            />
            <YAxis
              tickFormatter={(price) => `$${price.toFixed(2)}`}
            />
            <Tooltip content={<HoverLabel />} />
            <Line
              type="stepAfter"
              dataKey="price"
              stroke="#4299e1"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 8, stroke: '#4299e1', fill: '#fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="text-center text-gray-500 py-20">
          Price history for this product is empty.
        </div>
      )}
    </div>
  );

}
