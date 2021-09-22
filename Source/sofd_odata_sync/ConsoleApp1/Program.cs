using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Simple.OData.Client;

namespace ConsoleApp1
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Uri u = new Uri("http://services.odata.org/V4/TripPinServiceRW/");

            var client = new ODataClient("http://services.odata.org/V4/TripPinServiceRW/");

            var x = ODataDynamic.Expression;
            IEnumerable<dynamic> values = await client
                .For(x.Photos)
                .FindEntriesAsync();

            foreach (var photo in values)
            {
                Console.WriteLine(photo.Name);
            }
        }
    }
}
