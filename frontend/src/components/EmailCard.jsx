export default function EmailCard({ correo }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-4 border-l-4 border-blue-500">
      <h2 className="font-bold text-lg">{correo.asunto}</h2>
      <p className="text-gray-700 mt-2">{correo.cuerpo.slice(0, 200)}...</p>
      <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full mt-2 inline-block">
        {correo.categoria}
      </span>
    </div>
  );
}
