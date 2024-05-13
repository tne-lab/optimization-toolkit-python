using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;

namespace DatabaseConsoleApplication
{
    internal class Program
    {

            static void Main(string[] args)
            {
                // Create the service collection and configure services
                var services = ConfigureServices();

                // Build the service provider
                using (var serviceProvider = services.BuildServiceProvider())
                {
                    // Get the AppDbContext service from the service provider
                    using (var scope = serviceProvider.CreateScope())
                    {
                        var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

                        // Check if the database is connected
                        if (dbContext.IsDatabaseConnected())
                        {
                            Console.WriteLine("Database connection established.");

                            // Add a sample product
                            Addtablesample(dbContext);
                            Updatetablesample(dbContext);
                            deletetablesample(dbContext);
                        }
                        else
                        {
                            Console.WriteLine("Unable to connect to the database.");
                            // Handle the failure scenario
                            // For example, you can log the error and exit the application
                            // Log.Error("Unable to connect to the database.");
                            // Environment.Exit(1);
                        }
                    }
                }
            }

            static IServiceCollection ConfigureServices()
            {
                // Create the service collection
                var services = new ServiceCollection();

                // Add database context with configuration
                services.AddDbContext<AppDbContext>(options =>
                    options.UseNpgsql("host=127.0.0.1;port=5432;database=postgres;username=postgres;password=xxxx;sslmode=prefer"));

                return services;
            }

        // functions to perform CRUD
            static void Addtablesample(AppDbContext dbContext)
            {
                var product = new Product
                {
                    Name = "Sample Product",
                    Price = 1.31m
                };

                dbContext.Products.Add(product);
                dbContext.SaveChanges();
                Console.WriteLine("Sample product added to the database.");
            }
            static void Updatetablesample(AppDbContext dbContext)
            {
                // Update operation
                var productToUpdate = dbContext.Products.FirstOrDefault(p => p.Id == 1);
                if (productToUpdate != null)
                {
                    productToUpdate.Price = 164564.99m;
                    dbContext.SaveChanges();
                    Console.WriteLine("Product updated successfully.");
                }
                else
                {
                    Console.WriteLine("Product not found for update.");
                }
            }
            static void deletetablesample(AppDbContext dbContext)
            {
                // Delete operation
                var productToDelete = dbContext.Products.FirstOrDefault(p => p.Id == 4);
                if (productToDelete != null)
                {
                    dbContext.Products.Remove(productToDelete);
                    dbContext.SaveChanges();
                    Console.WriteLine("Product deleted successfully.");
                }
                else
                {
                    Console.WriteLine("Product not found for delete.");
                }
            }

    }

    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }
        public DbSet<Product> Products { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder.UseNpgsql("host=127.0.0.1;port=5432;database=postgres;username=postgres;password=xxxx;sslmode=prefer");
        }

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

    public class Product
    {
        public int Id { get; set; }

        public string Name { get; set; }

        public decimal Price { get; set; }
    }
}
