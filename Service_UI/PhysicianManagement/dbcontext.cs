using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace WSPHY
{
    public class DRADbContext : DbContext
    {
        // declaration
        // database table references

        public DbSet<SessionInfo> SessionInfos { get; set; }
        // protected functions
        // This is where we configure the connection string, need to figure out security/ encryption aspect
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            // remember : Tools, Design, json and file extension
            // Also copy the appsetting.json in properties
           IConfigurationRoot configuration = new ConfigurationBuilder()
          .SetBasePath(Directory.GetCurrentDirectory())
          .AddJsonFile("appsettings.json")
          .Build();
            var connectionString = configuration.GetConnectionString("DefaultConnection");
            optionsBuilder.UseNpgsql(connectionString);
        }

        // connection checker
        // checking if the database is connected or not
        public bool IsDatabaseConnected()
        {
            try
            {
                Database.OpenConnection();
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
