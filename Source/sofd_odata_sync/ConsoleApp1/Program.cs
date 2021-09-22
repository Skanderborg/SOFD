using System;
using System.Threading.Tasks;
using Simple.OData.Client;

namespace ConsoleApp1
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Uri u = new Uri("https://packages.nuget.org/v1/FeedService.svc");
            var client = new ODataClient(u);
            var packages = await client.FindEntriesAsync("Packages?$filter=Title eq 'Simple.OData.Client'");
            foreach (var package in packages)
            {
                Console.WriteLine(package["Title"]);
            }
        }
    }
}
