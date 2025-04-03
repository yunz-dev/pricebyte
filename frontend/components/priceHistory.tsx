import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';


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

interface ChartDataItem {
  date: string;
  price: number;
}

/**
 * Renders an interactive line chart showing the price history of a product over time.
 */
export default function PriceHistory({ params }: PriceHistoryProps) {
  
  // Chart data array to hold date points and prices
  const chartData: ChartDataItem[] = [];

  // Label that pops up on price history hover
  const HoverLabel = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const price = payload[0].value;
      return (
        <div className="p-3 bg-white border border-gray-200 rounded-lg shadow-xl">
          <p className="font-bold text-gray-900">{`$${price.toFixed(2)}`}</p>
          <p className="text-sm text-gray-600">{new Date(label).toLocaleDateString('en-AU', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
          })}</p>
        </div>
      );
    }
  };
  
  // Data logic to create chartData array - simplified approach
  params.priceHistory.forEach(entry => {
    const startDate = new Date(entry.startDate);
    const endDate = new Date(entry.endDate);
    
    // Add start point
    chartData.push({
      date: startDate.getTime(),
      price: entry.price,
    });
    
    // Add end point only if it's different from start
    if (endDate.getTime() !== startDate.getTime()) {
      chartData.push({
        date: endDate.getTime(),
        price: entry.price,
      });
    }
  });
  
  // Remove duplicates and sort
  const uniqueData = chartData.reduce((acc: ChartDataItem[], current) => {
    const existing = acc.find((item: ChartDataItem) => item.date === current.date);
    if (!existing) {
      acc.push(current);
    }
    return acc;
  }, []);
  
  uniqueData.sort((a, b) => a.date - b.date);

  const finalData = uniqueData.length > 0 ? uniqueData : chartData;

  return (
    <div className="w-full">
      {finalData.length > 0 ? (
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={finalData} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" className="opacity-30" />
            <XAxis
              dataKey="date"
              type="number"
              domain={['dataMin', 'dataMax']}
              scale="time"
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-AU', { 
                month: 'short', 
                year: '2-digit' 
              })}
              tick={{ fontSize: 12 }}
              axisLine={{ stroke: '#e5e7eb' }}
              tickLine={{ stroke: '#e5e7eb' }}
            />
            <YAxis
              domain={['dataMin - 0.5', 'dataMax + 0.5']}
              tickFormatter={(price) => `$${price.toFixed(2)}`}
              tick={{ fontSize: 12 }}
              axisLine={{ stroke: '#e5e7eb' }}
              tickLine={{ stroke: '#e5e7eb' }}
            />
            <Tooltip content={<HoverLabel />} />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={false}
              activeDot={{ 
                r: 6, 
                stroke: '#3b82f6', 
                strokeWidth: 2,
                fill: '#ffffff',
                style: { filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }
              }}
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="text-center text-gray-500 py-20">
          <div className="text-lg font-medium">No price history available</div>
          <div className="text-sm mt-2">Price data will appear here when available</div>
        </div>
      )}
    </div>
  );

}
