export interface Item {
  id: number;
  values?: number[];
}

export interface ItemViewerProps {
  items: Item[];
  showValues: boolean;
}

export const ItemViewer = ({ items, showValues }: ItemViewerProps) => {
  console.log(items);
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          {showValues && <th>Values</th>}
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id}>
            <td>{item.id}</td>
            {showValues && (
              <td>
                {item.values && item.values.join(", ")}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </table>
  );
};